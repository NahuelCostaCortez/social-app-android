package es.uniovi.amigos;

import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.support.v4.content.LocalBroadcastManager;
import android.widget.EditText;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.firebase.iid.FirebaseInstanceId;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private List<Amigo> amigos;
    private String url;
    String mUserName = null;
    int id = -1;
    BroadcastReceiver mHandlerForBroadcast = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        // Actualizar las posiciones cada cierto tiempo
        //Timer timer = new Timer();
        //TimerTask updateAmigos = new UpdateAmigosPosition();
        //timer.scheduleAtFixedRate(updateAmigos, 0, 100);
        askUserName();
        ActivityCompat.requestPermissions(this,new String[]{
                android.Manifest.permission.ACCESS_FINE_LOCATION
        }, 1);

        mHandlerForBroadcast = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                System.out.println("Broadcast: received = " + intent.getAction());
                getAmigosList();
            }
        };
        LocalBroadcastManager.getInstance(this).registerReceiver(
                mHandlerForBroadcast,
                new IntentFilter("updateFromServer"));
    }

    @Override
    protected void onResume() {
        super.onResume();
        LocalBroadcastManager.getInstance(this).registerReceiver(
                mHandlerForBroadcast,
                new IntentFilter("updateFromServer"));
    }

    @Override
    protected void onPause() {
        LocalBroadcastManager.getInstance(this).unregisterReceiver(mHandlerForBroadcast);
        super.onPause();
    }

    private void getAmigoId() {
        // Crear la cola de peticiones HTTP
        RequestQueue queue = Volley.newRequestQueue(this);

        // Crear una petición
        String url ="https://utor.serveo.net/api/amigo/byName/"+this.mUserName;
        JsonObjectRequest jsonRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                // Implementar el interfaz Listener que debe tener el método
                // onResponse, que será llamado al recibir la respuesta del servidor
                // Este método se ejecutará en el hilo del GUI
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            id = response.getInt("id");
                            System.out.println("Recibo el id de amigo: "+id);
                            updateDeviceToken();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                // Implementar el interfaz ErrorListener, que debe tener el método
                // onErrorResponse, que será llamado si la respuesta del servidor no es 200 OK
                // También se ejecutará en la interfaz de usuario
                new Response.ErrorListener(){
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("Volley: ha ocurrido un error " + error);
                    }
                }
        );
        // Poner la petición en la cola
        queue.add(jsonRequest);
    }

    private void updateLocation(double lati, double longi) {
        // Crear la cola de peticiones HTTP
        RequestQueue queue = Volley.newRequestQueue(this);

        // Crear una petición
        JSONObject jsonToSend = new JSONObject();
        try {
            jsonToSend.put("id", id);
            jsonToSend.put("lati", lati);
            jsonToSend.put("longi", longi);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        System.out.println("Llego a actualizar la localización con lati: "+lati +"y longi: "+longi);
        String url_put = "https://utor.serveo.net/api/amigo/"+this.id;

        JsonObjectRequest objectRequest = new JsonObjectRequest(Request.Method.PUT, url_put, jsonToSend,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                            System.out.println("Actualizo la localizacion en BD: "+id);
                    }
                },
                // Implementar el interfaz ErrorListener, que debe tener el método
                // onErrorResponse, que será llamado si la respuesta del servidor no es 200 OK
                // También se ejecutará en la interfaz de usuario
                new Response.ErrorListener(){
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("Volley: ha ocurrido un error " + error);
                    }
                }
        );
        // Poner la petición en la cola
        queue.add(objectRequest);
    }

    void getAmigosList(){
        // Crear la cola de peticiones HTTP
        RequestQueue queue = Volley.newRequestQueue(this);

        // Crear una petición
        String url ="https://utor.serveo.net/api/amigos";
        JsonArrayRequest jsonRequest = new JsonArrayRequest(Request.Method.GET, url, null,
                // Implementar el interfaz Listener que debe tener el método
                // onResponse, que será llamado al recibir la respuesta del servidor
                // Este método se ejecutará en el hilo del GUI
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            amigos = new ArrayList<Amigo>();
                            //System.out.println("Obtenida respuesta con length: "+response.length());
                            for(int i = 0; i< response.length(); i++){
                                Amigo a = new Amigo();
                                //System.out.println("Añado al amigo con nombre: "+response.getJSONObject(i).getString("name")+
                                //"con longitud:" +response.getJSONObject(i).getDouble("longi")+"y con latitud: "+response.getJSONObject(i).getDouble("lati"));
                                a.setNombre(response.getJSONObject(i).getString("name"));
                                a.setLatitud(response.getJSONObject(i).getDouble("lati"));
                                a.setLongitud(response.getJSONObject(i).getDouble("longi"));
                                amigos.add(a);
                            }
                            paintAmigosList();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                // Implementar el interfaz ErrorListener, que debe tener el método
                // onErrorResponse, que será llamado si la respuesta del servidor no es 200 OK
                // También se ejecutará en la interfaz de usuario
                new Response.ErrorListener(){
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("Volley: ha ocurrido un error " + error);
                    }
                }
        );
        // Poner la petición en la cola
        queue.add(jsonRequest);
    }

    public void updateDeviceToken(){
        if(this.id == -1)
            return;
        String token = FirebaseInstanceId.getInstance().getToken();
        if(token == null)
            return;
        System.out.println("Device Token:"+token);
        // Crear la cola de peticiones HTTP
        RequestQueue queue = Volley.newRequestQueue(this);

        // Crear una petición
        JSONObject jsonToSend = new JSONObject();
        try {
            jsonToSend.put("device", token);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        String url_put = "https://utor.serveo.net/api/amigo/"+this.id;

        JsonObjectRequest objectRequest = new JsonObjectRequest(Request.Method.PUT, url_put, jsonToSend,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("Hecho el put para device");
                    }
                },
                // Implementar el interfaz ErrorListener, que debe tener el método
                // onErrorResponse, que será llamado si la respuesta del servidor no es 200 OK
                // También se ejecutará en la interfaz de usuario
                new Response.ErrorListener(){
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("Volley: ha ocurrido un error " + error);
                    }
                }
        );
        // Poner la petición en la cola
        queue.add(objectRequest);
    }

    public void onRequestPermissionsResult(int requestCode, String permissions[],
                                           int[] grantResults) {
        switch (requestCode) {
            case 1: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // Tenemos permiso
                    // llamamos a una función que creará las
                    // peticiones de localización
                    SetupLocation();
                } else {
                    // No tenemos permiso... no hacemos nada especial
                    // en esta aplicación para ese caso
                }
                return;
            }
            // La función podría usarse para recibir más permisos, pero
            // no es el caso en esta aplicación
        }
    }

    void SetupLocation() {
        if (ActivityCompat.checkSelfPermission(this,
                android.Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(this,
                android.Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED)
        {
            // Verificar por si acaso si tenemos el permiso, y si no
            // no hacemos nada
            return;
        }


        // Se debe adquirir una referencia al Location Manager del sistema
        LocationManager locationManager =
                (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);

        // Se obtiene el mejor provider de posición
        Criteria criteria = new Criteria();
        String  provider = locationManager.getBestProvider(criteria, false);

        // Se crea un listener de la clase que se va a definir luego
        MyLocationListener locationListener = new MyLocationListener();

        // Se registra el listener con el Location Manager para recibir actualizaciones
        // En este caso pedimos que nos notifique la nueva localización
        // si el teléfono se ha movido más de 10 metros
        locationManager.requestLocationUpdates(provider, 0, 10, locationListener);

        // Comprobar si se puede obtener la posición ahora mismo
        Location location = locationManager.getLastKnownLocation(provider);
        if (location != null) {
            // La posición actual es location
        } else {
            // Actualmente no se puede obtener la posición
        }
    }

    // Se define un Listener para escuchar por cambios en la posición
    class MyLocationListener implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {
            // Se llama cuando hay una nueva posición para ese location provider
            System.out.println("GPS changed");
            double lati = location.getLatitude();
            double longi = location.getLongitude();
            // Se actualiza la posición en la base de datos
            if(id != -1) {
                System.out.println("Se tiene el identificar del usuario");
                updateLocation(lati, longi);
            }

        }

        // Se llama cuando cambia el estado
        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {}

        // Se llama cuando se activa el provider
        @Override
        public void onProviderEnabled(String provider) {}

        // Se llama cuando se desactiva el provider
        @Override
        public void onProviderDisabled(String provider) {}
    }

    private void paintAmigosList() {
        for(int i = 0; i< amigos.size(); i++){
            mMap.addMarker(new MarkerOptions()
                            .position(new LatLng(amigos.get(i).getLatitud(), amigos.get(i).longitud)));
        }

    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng sydney = new LatLng(-34, 151);
        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));

        mMap.addMarker(new MarkerOptions()
                .position(new LatLng(10, 10)));
        getAmigosList();
    }

    public void askUserName() {
        AlertDialog.Builder alert = new AlertDialog.Builder(this);

        alert.setTitle("Settings");
        alert.setMessage("User name:");

        // Crear un EditText para obtener el nombre
        final EditText input = new EditText(this);
        alert.setView(input);

        alert.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int i) {
                mUserName = input.getText().toString();
                getAmigoId();
            }
        });

        alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int i) {
                // Canceled.
            }
        });

        alert.show();
    }

    class UpdateAmigosPosition extends TimerTask {
        public void run() {
            getAmigosList();
        }
    }
}

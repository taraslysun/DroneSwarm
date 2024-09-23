﻿using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class DroneController : MonoBehaviour
{
    public int id;  // Unique ID for each drone
    // public int port = 50000 + id;  // Port number for each drone 1
    public int port;

    private UdpClient udpClient;
    private Thread udpListenerThread;
    private Vector3 targetPosition;
    private bool positionUpdated = false;

    void Start()
    {
        // Initialize target position
        targetPosition = transform.position;

        // Start the UDP server
        udpListenerThread = new Thread(new ThreadStart(UDPListen));
        udpListenerThread.IsBackground = true;
        udpListenerThread.Start();
        //port = 50000 + id;
    }

    void Update()
    {
        // Set the position of the drone to the target position
        if (positionUpdated)
        {
            transform.position = targetPosition;
            positionUpdated = false;
        }
    }

    private void UDPListen()
    {
        udpClient = new UdpClient(port); // Listen on port port
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, port);

        while (true)
        {
            try
            {
                // Listen for incoming data
                byte[] data = udpClient.Receive(ref remoteEndPoint);
                string message = Encoding.UTF8.GetString(data);
                // Print message
                //Debug.Log("Received message: " + message);

                // Parse the JSON message to get the coordinates
                ProcessMessage(message);
            }
            catch (Exception e)
            {
                Debug.LogError("UDP Listener Error: " + e.Message);
            }
        }
    }

    private void ProcessMessage(string message)
    {
        try
        {
            // Assuming the message is in JSON format: {"id": 1, "latitude":0, "longitude":0, "altitude":0}
            var jsonData = JsonUtility.FromJson<CoordinateData>(message);
            
            // Check if the message is for this drone
            if (jsonData.id == this.id)
            {
                targetPosition = new Vector3(jsonData.latitude, jsonData.altitude, jsonData.longitude);
                positionUpdated = true;
                // Print "Received new position: " + targetPosition 
                //Debug.Log($"Drone {id} received new target position: {targetPosition}");
            }
        }
        catch (Exception e)
        {
            Debug.LogError("Error processing message: " + e.Message);
        }
    }

    void OnApplicationQuit()
    {
        // Clean up the UDP client and thread on exit
        udpListenerThread.Abort();
        udpClient.Close();
    }

    [Serializable]
    public class CoordinateData
    {
        public int id;  // Drone ID
        public float latitude;
        public float longitude;
        public float altitude;
    }
}
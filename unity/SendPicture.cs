using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

public class SendPicture : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    
    public Camera droneCamera;
    private HttpClient httpClient;
    public string ip;
    public int port;
    int i = 0;
    void Start()
    {
        httpClient = new HttpClient();
        droneCamera = GetComponentInChildren<Camera>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        if (i++ % 10  == 0 ){
            Send();
            i %= 10;
        }
    }
    
    private void Send()
    {
        StartCoroutine(SendPictureCoroutine());
    }

    private IEnumerator SendPictureCoroutine()
    {
        // Capture the frame from the camera
        yield return new WaitForEndOfFrame();

        RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        droneCamera.targetTexture = renderTexture;
        Texture2D screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        droneCamera.Render();
        RenderTexture.active = renderTexture;
        screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenShot.Apply();

        // Convert the Texture2D to a byte array (JPG format)
        byte[] imageBytes = screenShot.EncodeToJPG();

        // Clean up
        droneCamera.targetTexture = null;
        RenderTexture.active = null;
        Destroy(renderTexture);

        // Call the async method to send the image
        Task.Run(() => SendImageAsync(imageBytes));
    }

    private async Task SendImageAsync(byte[] imageBytes)
    {
        try
        {
            MultipartFormDataContent form = new MultipartFormDataContent();
            form.Add(new ByteArrayContent(imageBytes), "file", "image.jpg");

            var response = await httpClient.PostAsync("http://" + ip + ":" + port + "/", form);

            if (response.IsSuccessStatusCode)
            {
                Debug.Log("Image sent successfully!");
            }
            else
            {
                Debug.Log("Failed to send image: " + response.ReasonPhrase);
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError("Exception caught: " + ex.Message);
        }
    }

    private void OnApplicationQuit()
    {
        httpClient.Dispose();
    }
}
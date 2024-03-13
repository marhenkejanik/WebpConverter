package org.example;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class WebpConverter
{
    static
    {
        // Load OpenCV native library
        System.load("YourPathToYourOpenCV");
    }

    public static void main(String[] args) throws IOException
    {
        String sourceFolderPath = "YourPathToADirectory";
        String targetFolderPath = "YourPathToADirectory";

        convertExistingWebpFiles(sourceFolderPath, targetFolderPath);

        while(true) {
            monitorFolder(sourceFolderPath, targetFolderPath);
            sleepForSeconds(2); // Adding a 2-second delay so it doesnt convert a file that is being downloaded resulting in an error
        }
    }

    private static void convertExistingWebpFiles(String sourceFolderPath, String targetFolderPath)
    {
        File sourceFolder = new File(sourceFolderPath);
        File[] files = sourceFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(".webp"));
        if (files != null)
        {
            for (File file : files)
            {
                convertWebpToPng(file, targetFolderPath);
            }
        }
    }

    private static void monitorFolder(String sourceFolderPath, String targetFolderPath)
    {
        File sourceFolder = new File(sourceFolderPath);
        File[] files = sourceFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(".webp"));
        if (files != null)
        {
            for (File file : files)
            {
                convertWebpToPng(file, targetFolderPath);
            }
        }
    }

    private static void convertWebpToPng(File webpFile, String targetFolderPath) {
        String inputFilePath = webpFile.getAbsolutePath();
        String outputFileName = webpFile.getName().replace(".webp", ".png");
        String outputFilePath = targetFolderPath + File.separator + outputFileName;
 
        Mat webpMat = Imgcodecs.imread(inputFilePath);

        Imgcodecs.imwrite(outputFilePath, webpMat);
        webpFile.delete();
    }
    private static void sleepForSeconds(int seconds)
    {
        try
        {
            TimeUnit.SECONDS.sleep(seconds);
        }
        catch (InterruptedException e)
        {
            Thread.currentThread().interrupt();
        }
    }
}

package util;
/*File AudioRecorder02.java
Copyright 2003, Richard G. Baldwin

This program demonstrates the capture of audio
data from a microphone into an audio file.

A GUI appears on the screen containing the
following buttons:
  Capture
  Stop

In addition, five radio buttons appear on the
screen allowing the user to select one of the
following five audio output file formats:

  AIFC
  AIFF
  AU
  SND
  WAVE

When the user clicks the Capture button, input
data from a microphone is captured and saved in
an audio file named junk.xx having the specified
file format.  (xx is the file extension for the
specified file format.  You can easily change the
file name to something other than junk if you
choose to do so.)

Data capture stops and the output file is closed
when the user clicks the Stop button.

It should be possible to play the audio file
using any of a variety of readily available
media players, such as the Windows Media Player.

Not all file types can be created on all systems.
For example, types AIFC and SND produce a "type
not supported" error on my system.

Be sure to release the old file from the media
player before attempting to create a new file
with the same extension.

Tested using SDK 1.4.1 under Win2000
************************************************/

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import javax.sound.sampled.*;

public class AudioCapture extends JFrame{

	public static void main(String[] args)
	{
		try {
			AudioFormat format = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 44100, 16, 2, 4, 44100, false);
			DataLine.Info dataInfo = new DataLine.Info(TargetDataLine.class, format);
			if(!AudioSystem.isLineSupported(dataInfo))
			{
				System.out.println("Not Supported");
			}
			TargetDataLine targetLine = (TargetDataLine)AudioSystem.getLine(dataInfo);
			targetLine.open();
			
			JOptionPane.showMessageDialog(null, "hit ok to start recording");
			targetLine.start();
			
			Thread audioRecorderThread = new Thread()
			{
				@Override
				public void run()
				{
					AudioInputStream recordingStream = new AudioInputStream(targetLine);
					File outputFile = new File("record.wav");
					try {
						AudioSystem.write(recordingStream, AudioFileFormat.Type.WAVE, outputFile);
					}catch(Exception ex)
					{
						ex.printStackTrace();
					}
					System.out.println("stopped recording");
				}
			};
			audioRecorderThread.start();
			JOptionPane.showMessageDialog(null, "hit ok to stop recording");
			targetLine.stop();
			targetLine.close();
	    } catch (Exception e) {
	        e.printStackTrace();
	    } 
	}
}
package util;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

import javax.sound.midi.Instrument;
import javax.sound.midi.MidiChannel;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.Synthesizer;

import representation.Measure;
import representation.Note;
import representation.Pitch;

public class SoundHandler {

	Instrument[] instr;
	MidiChannel[] mChannels;

	Synthesizer midiSynth;

	private static List<String> notes = Arrays.asList("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B");
	private static MidiChannel[] channels;
	private static int INSTRUMENT = 0; // 0 is a piano, 9 is percussion, other channels are for other instruments
	private static int VOLUME = 80; // between 0 et 127

	public SoundHandler(){

		try {
			// * Open a synthesizer
			Synthesizer synth = MidiSystem.getSynthesizer();
			synth.open();
			channels = synth.getChannels();
			instr = synth.getDefaultSoundbank().getInstruments();
			synth.loadInstrument(instr[71]);
		}
		catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	public void playMeasureAsync(Measure measure)
	{
		int BPM = measure.tempo.beatsPerMinute;
		Rational millisPerBeat = new Rational(60000,BPM);
		Queue<noteEvent> que = new LinkedList<noteEvent>();
		Rational totalBeats = new Rational(0,1);
		for(Note note: measure.notes)
		{
			int denom = note.lengthDenominator;
			Rational numBeats = new Rational(1,denom).multiply(new Rational(measure.timeSignature.denominator, 1));
			Rational startTime = totalBeats.multiply(millisPerBeat);
			totalBeats = totalBeats.add(numBeats);
			Rational endTime = totalBeats.multiply(millisPerBeat);
			que.add(new noteEvent(startTime, true, note.pitch));
			que.add(new noteEvent(endTime, false, note.pitch));
		}
		long startTimeMillis = System.currentTimeMillis();
		System.out.println(que);
		while(!que.isEmpty())
		{
			noteEvent e = que.peek();
			if(e.time.lessThan(System.currentTimeMillis() - startTimeMillis))
			{
				que.poll();
				if(e.start) {
					noteOn(e.pitch);
					System.out.println(e.pitch.chromaticNumber);
				}
				else
					noteOff(e.pitch);
			}
		}
	}

	private class noteEvent{

		Rational time;
		boolean start;
		Pitch pitch;

		public noteEvent(Rational time, boolean start, Pitch pitch)
		{
			this.time = time;
			this.start = start;
			this.pitch = pitch;
		}

		public String toString()
		{
			return "("+time+" "+start+" "+pitch.chromaticNumber+")";
		}

	}

	public void noteOn(Pitch pitch)
	{
		if(pitch != Pitch.REST)
			channels[INSTRUMENT].noteOn(pitch.chromaticNumber + 67, VOLUME );
	}

	public void noteOff(Pitch pitch)
	{
		if(pitch != Pitch.REST)
			channels[INSTRUMENT].noteOff(pitch.chromaticNumber + 67);
	}



}

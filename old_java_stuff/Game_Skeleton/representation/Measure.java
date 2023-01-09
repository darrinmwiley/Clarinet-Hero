package representation;
import java.util.ArrayList;

import util.Rational;

public class Measure {
	
	public Tempo tempo;
	public TimeSignature timeSignature;
	public ArrayList<Note> notes;
	
	public Measure(Tempo tempo, TimeSignature timeSignature)
	{
		this.tempo = tempo;
		this.timeSignature = timeSignature;
		this.notes = new ArrayList<Note>();
	}
	
	public Measure()
	{
		this(new Tempo(60), new TimeSignature(4,4));
	}
	
	public boolean validate()
	{
		Rational beats = countBeats();
		return beats.denom == 1 && beats.num == timeSignature.numerator;
	}
	
	public Rational countBeats()
	{
		Rational beatCount = new Rational(0,1);
		for(Note note: notes)
		{
			int denom = note.lengthDenominator;
			beatCount = beatCount.add(new Rational(1,denom).multiply(new Rational(timeSignature.denominator, 1)));
		}
		return beatCount;
	}
	
}

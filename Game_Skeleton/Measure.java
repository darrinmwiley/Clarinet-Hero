import java.util.ArrayList;

public class Measure {
	
	Tempo tempo;
	TimeSignature timeSignature;
	Clef clef;
	ArrayList<Note> notes;
	
	public Measure(Tempo tempo, TimeSignature timeSignature, Clef clef)
	{
		this.tempo = tempo;
		this.timeSignature = timeSignature;
		this.clef = clef;
		this.notes = new ArrayList<Note>();
	}
	
	public Measure()
	{
		this(new Tempo(60), new TimeSignature(4,4), Clef.TREBLE);
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

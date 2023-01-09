package representation;

public class TimeSignature {
	public int numerator; // beatsPerMeasure 
	public int denominator; // beat note
	
	public TimeSignature(int beatsPerMeasure, int beatNote)
	{
		this.numerator = beatsPerMeasure;
		this.denominator = beatNote;
	}
}

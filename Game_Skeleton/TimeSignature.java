
public class TimeSignature {
	int numerator; // beatsPerMeasure 
	int denominator; // beat note
	
	public TimeSignature(int beatsPerMeasure, int beatNote)
	{
		this.numerator = beatsPerMeasure;
		this.denominator = beatNote;
	}
}

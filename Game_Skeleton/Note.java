
public class Note {
	
	//TODO: accents and other stuff
	//TODO: dots
	
	//note is expressed in relation to quarter note
	
	int lengthDenominator;
	Pitch pitch;
	
	
	public Note(int lengthDenominator, Pitch pitch)
	{
		this.lengthDenominator = lengthDenominator;
		this.pitch = pitch;
	}
	
}

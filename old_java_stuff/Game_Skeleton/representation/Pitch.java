package representation;

public class Pitch {
	
	public static Pitch REST = new Pitch(-42069);
	public int chromaticNumber;
	//0 is clarinet open G (G4 midi 67)
	public Pitch(int chromaticNumber)
	{
		this.chromaticNumber = chromaticNumber;
	}
	
	public String toString()
	{
		return "TODO IMPLEMENT";
	}
}

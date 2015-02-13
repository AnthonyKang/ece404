public class Card{
	public enum Suit {
		CLUBS(1), SPADES(2)
		int value;
		private Suit(int v) {value = v;}
	}

	private int card;

	public Card(int r, Suit s){
		card = r;
		suit = s;
	}
	public int value() {return card;}
}
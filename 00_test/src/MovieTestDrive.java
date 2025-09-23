class Movie {
    String title;
    String genre;
    int rating;

    void palyIt() {
        // method example in class
        // when use the parameter in Movie class, use 'this.[parameter]'.
        System.out.println("Playing the movie named " + this.title + ".");
    }
}


public class MovieTestDrive {
    public static void main(String[] args) {
        // first movie
        Movie one = new Movie();
        one.title = "Gone with the Stock";
        one.genre = "Tragic";
        one.rating = -2;

        // second movie
        Movie two = new Movie();
        two.title = "Lost in Cubicle Space";
        two.genre = "Comedy";
        two.rating = 5;
        two.palyIt();

        // third movie
        Movie three = new Movie();
        three.title = "Byte Club";
        three.genre = "Tragic but ultimately uplifting";
        three.rating = 127;
    }
}

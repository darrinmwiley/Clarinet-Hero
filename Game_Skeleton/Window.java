/**
 * Created by Reaper on 5/22/17.
 */
import javax.swing.JFrame;
import java.awt.Canvas;
import java.awt.Dimension;

public class Window extends Canvas {

    public Window(int width, int height, String title, Game g){

            JFrame frame = new JFrame(title); // make new JFrame instance

            frame.setPreferredSize(new Dimension(width, height));
            frame.setMaximumSize(new Dimension(width, height));
            frame.setMinimumSize(new Dimension(width, height));

            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // corner exit
            frame.setResizable(false);
            frame.setLocationRelativeTo(null); // makeswindow start in center versus top left
            frame.add(g); // adding game class into fram
            frame.setVisible(true); // set fram visible so we see it
            g.start(); // run start method

        }



}

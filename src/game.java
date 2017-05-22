import java.awt.*;
import java.awt.image.BufferStrategy;

/**
 * Created by Reaper on 5/22/17.
 */
public class game extends Canvas implements Runnable{


    public static final int WIDTH = 640, HEIGHT = WIDTH / 12 * 9; // nice aspect ratio

    private Thread thread; // entire game will run through this thread, single threaded is not the best
    private boolean running = false;


    // Constructor
    public game(){
        new window(WIDTH, HEIGHT, "GAME TIME!", this);
    }

    public synchronized void start(){
        thread = new Thread(this);
        thread.start();
        running = true;
    }

    public synchronized void stop(){
        try{
            thread.join();

        }catch(Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public void run() {

        //we need a loop that performs 2 things:
        // - it checks whether enough time has passed (1/60 sec) to refresh the game
        //  - checks whether enough time has passed (1 sec) to refresh the FPS counter

        // while 'running' the loop adds the time it took to go through one iteration of the
        // loop then adds it to delta (which is simplified to 1) so once it reaches
        // 1 delta it means enough time has passed to go forward one tick.

        long lastTime = System.nanoTime(); // start time to measure time passed
        double amountOfTicks = 60.0; // ticks per second
        double ns = 1000000000 / amountOfTicks; // nanoseconds between ticks
        double delta = 0; // time between ticks
        long timer = System.currentTimeMillis();
        int frames = 0; // number of frames per second

        while(running) {
            long now = System.nanoTime();
            delta += (now - lastTime) / ns; // update delta to time passed since last iter of loop
            lastTime = now;

            // while we are behind on game ticks
            while (delta >= 1) {
                tick(); // make it tick
                delta--;
            }

            // redraw screen
            if (running) // maybe we should only render if an update has occured or a tick?
                render();
            // increase fps by one
            frames++;

            // if one second has passed
            if (System.currentTimeMillis() - timer > 1000) {
                timer += 1000;
                System.out.println("FPS: " + frames); // display FPS
                frames = 0; // reset FPS counter to one
            }
        }
        stop();
    }

    private void tick(){

    }

    private void render(){
        BufferStrategy bs = this.getBufferStrategy();
        if(bs == null) {
            this.createBufferStrategy(3);
            return;
        }
        Graphics g = bs.getDrawGraphics();
        g.setColor(Color.black);
        g.fillRect(0, 0, WIDTH, HEIGHT);

        g.dispose();
        bs.show();



    }





    public static void main(String[] args) {

        new game();


    }
}

import java.awt.*;

/**
 * Created by Reaper on 5/22/17.
 */

// enemies, players, coins, anything is a game object
public abstract class GameObject {
    protected int x, y; // can only be accessed by which object inherets the GameObject
    protected ID id;
    protected  int velX, velY;

    public  GameObject(int  x, int y, ID id){
        this.x = x;
        this.y = y;
        this.id = id;
    }

    public abstract void tick(); // you need to use it in all the classes
    public abstract void render(Graphics g);


    // All of these are in Player, Enemy etc class
    public void setX(int x){
        this.x = x;
    }

    public void setY(int y) {
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public void setId(ID id) {
        this.id = id;
    }

    public ID getId() {
        return id;
    }

    public void setVelX(int velX) {
        this.velX = velX;
    }

    public void setVelY(int velY) {
        this.velY = velY;
    }

    public int getVelX() {
        return velX;
    }

    public int getVelY() {
        return velY;
    }
}

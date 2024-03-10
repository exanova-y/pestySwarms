class Flower {
    PVector position; // Position of the flower
    boolean visited;  // Whether the flower has been visited

    Flower() {
        position = new PVector(random(width), random(height-50));
        visited = false;
    }

    void display() {
        fill(visited ? color(255, 0, 0) : color(0, 255, 0)); // Red if visited, green otherwise
        ellipse(position.x, position.y, 10, 10); // Draw the flower
    }
}

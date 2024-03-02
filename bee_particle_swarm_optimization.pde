// define constants
int NUM_FLOWERS = 100;
int NUM_BEES = 50;
float EXPLORE_EXPLOIT_RATIO = 0.1;

PVector gbest;

Flower[] flowers = new Flower[NUM_FLOWERS];
Bee[] bees = new Bee[NUM_BEES];


void setup() {
    size(1000, 600);
    
    for (int i = 0; i < NUM_FLOWERS; i++) {
        flowers[i] = new Flower();
    }
    for (int i = 0; i < NUM_BEES; i++) {
        bees[i] = new Bee();
    }
    gbest = new PVector(0, 0);
    
}

void draw() {
    background(255);
    textSize(20);
    fill(0);
    text("Green: pollinated", 10, height-15);
    text("Red: unpollinated", 200, height-15);
    text("Yellow: Bees", 400, height-15);
    //text(gbest, 50, 150);
    for (Flower flower : flowers) {
        flower.display();
      }
    for (Bee bee : bees) {
        bee.explore();
        bee.communicate();
        bee.update();
        bee.display();
    }
}

// notes: bees on the screen. add legend. more cross pollination maybe

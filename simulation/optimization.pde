int n = 20; // num of cells on each side
int padding = 10;
color[][] cells = new color[n][n]; //2d array, where each element stores a color value in the form of rgb
color[][] cellsNext = new color[n][n];

// crop colours
int r = 39; //red goes up to 145
int g = 166;
int b = 35;

int numPests;
int redOffset;
int blueOffset;
float infectProb = 0.15;

float blinksPerSecond = 20;
float cellSize;


void setup(){
  size(800, 800);
  frameRate(blinksPerSecond);
  cellSize = (height - 2*padding)/n;
  generateFields();
  
}

void draw(){
  background(0);
  infectFields();
  showFields();
}

void generateFields(){
  for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
      redOffset = int(random(-30, 40));
      blueOffset = int(random(-35, 25));
      cells[i][j] = color(r+redOffset, g, b+blueOffset);
    }
  }
}

void infectFields(){
  int count = 0;
  float prob;
  for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
     //color current = cells[i][j];
     //r = int(red(current));
     //g = int(green(current));
     //b = int(blue(current));
     
     //println(cells[i][j);
      //examines its neighbours
     redOffset = 0;
     
     count = countInfectedNeighbours(i, j); 
     prob = random(0, 1);
     if (count<3){ //the crop patch heals 
       redOffset -= count*10;
       r = max(r+redOffset, 1); //prevents red from going to 0
       cellsNext[i][j] = color(r, g, b);
       //println("counted less than 3 infected neighbours");
     }
     else if ((count==3 || count == 4) && prob < infectProb){ // infected neighbours
       redOffset += count*10; // the crop patch becomes infected
       r = min(r+redOffset, 145);  //red value is constrainted to be below 145
       cellsNext[i][j] = color(r, g, b);
       cells[i][j] = cellsNext[i][j];
       //println("counted >= 3 infected neighbours");
     }
    }
  }
}
  // cell next to cell now
  // select rand cell
  // rand cell propagates to max of k grids away like minesweeper

void showFields(){
  noStroke();
  for(int i=0; i<n; i++){
    float x = padding+i*cellSize;
    for(int j=0; j<n; j++){
      float y = padding+j*cellSize;
      fill(cells[i][j]);
      rect(x, y, cellSize, cellSize);
      
  }
}
}

int countInfectedNeighbours(int i, int j){
  int infectedNeighbours = 0;
  int infectionThres = 55;
  for(int p=-1; p<=1; p++){
    for(int q = -1; q<=1; q++){
      try{
        if ((red(cells[i+p][j+q]) > infectionThres) && !(p == 0 && q == 0)){
          infectedNeighbours++;
        }
      }
      catch (IndexOutOfBoundsException e){
      }
     }
  }
  return infectedNeighbours;
}


void mousePressed(){
  //println(mouseX, mouseY);
  int col = int((mouseX-padding)/cellSize);
  int row = int((mouseY-padding)/cellSize);
  if (mouseButton == LEFT && red(cells[col][row]) <= 135){
    //infect plant, red value is constrained to be <= 145
    redOffset += 20;
    //red(cellsNext[col][row]) += redOffset;
    println("human infection :o");
   
  }
  else if (mouseButton == RIGHT && red(cells[col][row]) >= 10){
    redOffset -= 10; // lowest r value in rgb is 0
    println("human healing :)");
  }
}

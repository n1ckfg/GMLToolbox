float delta = 1;

void updateControls() {
  if (keyPressed) {
    if (key == 'w') cam.pos.z -= delta;
    if (key == 's') cam.pos.z += delta;
    if (key == 'a') cam.pos.x -= delta;
    if (key == 'd') cam.pos.x += delta;
    if (key == 'q') cam.pos.y += delta;
    if (key == 'e') cam.pos.y -= delta;
  }
}
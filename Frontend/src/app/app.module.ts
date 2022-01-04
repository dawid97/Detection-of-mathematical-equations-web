import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { CanvasComponent } from './canvas/canvas.component';

@NgModule({
  imports: [BrowserModule, HttpClientModule],
  declarations: [AppComponent, CanvasComponent],
  bootstrap: [AppComponent]
})
export class AppModule {}

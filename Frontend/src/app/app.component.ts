import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  name = 'frontend';
  result: any;
  equation: any;

  public changedResult(result: any) {
    this.result = result;
  }

  changedEquation(equation: any) {
    this.equation = equation;
  }

  public onClear() {
    window.location.reload();
  }
}

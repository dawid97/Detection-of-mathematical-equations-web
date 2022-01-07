import { HttpClient } from '@angular/common/http';
import {
  Component,
  Input,
  ElementRef,
  AfterViewInit,
  ViewChild,
  Output,
  EventEmitter
} from '@angular/core';
import { fromEvent } from 'rxjs';
import { switchMap, takeUntil, pairwise } from 'rxjs/operators';

@Component({
  selector: 'app-canvas',
  template: '<canvas #canvas></canvas>',
  styles: ['canvas { opacity: 0.7; border-radius: 15px}']
})
export class CanvasComponent implements AfterViewInit {

  constructor(private http: HttpClient) { }

  @ViewChild('canvas') public canvas: ElementRef | undefined;

  @Input() public width = 800;
  @Input() public height = 600;
  @Output() public result = new EventEmitter();
  @Output() public equation = new EventEmitter();

  private cx: CanvasRenderingContext2D | null | undefined;

  public ngAfterViewInit() {
    const canvasEl: HTMLCanvasElement = this.canvas?.nativeElement;

    this.cx = canvasEl.getContext('2d');

    canvasEl.width = this.width;
    canvasEl.height = this.height;

    if (!this.cx) throw 'Cannot get context';

    this.cx.lineWidth = 3;
    this.cx.lineCap = 'round';
    this.cx.strokeStyle = '#000';

    this.cx.fillStyle = "white";
    this.cx.fillRect(0, 0, canvasEl.width, canvasEl.height);

    this.captureEvents(canvasEl);
  }

  private captureEvents(canvasEl: HTMLCanvasElement) {
    // this will capture all mousedown events from the canvas element
    fromEvent(canvasEl, 'mousedown')
      .pipe(
        switchMap(e => {
          // after a mouse down, we'll record all mouse moves
          return fromEvent(canvasEl, 'mousemove').pipe(
            // we'll stop (and unsubscribe) once the user releases the mouse
            // this will trigger a 'mouseup' event
            takeUntil(fromEvent(canvasEl, 'mouseup')),
            // we'll also stop (and unsubscribe) once the mouse leaves the canvas (mouseleave event)
            takeUntil(fromEvent(canvasEl, 'mouseleave')),
            // pairwise lets us get the previous value to draw a line from
            // the previous point to the current point
            pairwise()
          );
        })
      )
      .subscribe((res) => {
        const rect = canvasEl.getBoundingClientRect();
        const prevMouseEvent = res[0] as MouseEvent;
        const currMouseEvent = res[1] as MouseEvent;

        // previous and current position with the offset
        const prevPos = {
          x: prevMouseEvent.clientX - rect.left,
          y: prevMouseEvent.clientY - rect.top
        };

        const currentPos = {
          x: currMouseEvent.clientX - rect.left,
          y: currMouseEvent.clientY - rect.top
        };

        this.drawOnCanvas(prevPos, currentPos);
      });

    fromEvent(canvasEl, 'mouseup').pipe().subscribe(
      async () => {
        const imageUrl = canvasEl.toDataURL('image/png');
        // Leave only raw image data
        const imageData = imageUrl.substring(22);

        const reqBody = { img: imageData };
        this.http.post('http://localhost:8000/predict', reqBody).subscribe((res: any) => {
          console.log(res);
          res.result === 'NaN' ? this.result.emit("") : this.result.emit(res.result);
          this.equation.emit(res.equation);
        })
      }
    )
  }

  private drawOnCanvas(
    prevPos: { x: number; y: number },
    currentPos: { x: number; y: number }
  ) {
    if (!this.cx) {
      return;
    }

    this.cx.beginPath();

    if (prevPos) {
      this.cx.moveTo(prevPos.x, prevPos.y); // from
      this.cx.lineTo(currentPos.x, currentPos.y);
      this.cx.stroke();
    }
  }
}

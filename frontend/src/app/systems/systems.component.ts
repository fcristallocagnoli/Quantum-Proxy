import { Component } from '@angular/core';
import { System } from '@app/_models/system';
import { SystemService } from '@app/_services/system.service';
import { first } from 'rxjs';

@Component({
  selector: 'app-systems',
  templateUrl: './systems.component.html',
})
export class SystemsComponent {
  systems?: System[];
  showScroll: boolean = false;

  constructor(private systemService: SystemService) { }

  ngOnInit() {
    this.systemService.getAll()
      .pipe(first())
      .subscribe(systems => {
        console.log(systems);
        this.systems = systems;
      });
  }

}

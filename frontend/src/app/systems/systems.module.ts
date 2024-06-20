import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { SystemsRoutingModule } from './systems-routing.module';
import { SystemsComponent } from './systems.component';
import { ViewSystemComponent } from './view-system.component';
import { QueueComponent, StatusComponent } from '@app/_components/properties.component';

@NgModule({
    declarations: [
        SystemsComponent,
        ViewSystemComponent
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        SystemsRoutingModule,
        StatusComponent,
        QueueComponent
    ]
})
export class SystemsModule { }
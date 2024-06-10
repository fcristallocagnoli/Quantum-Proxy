import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SystemsComponent } from './systems.component';
import { ViewSystemComponent } from './view-system.component';


const routes: Routes = [
    { path: '', component: SystemsComponent },
    { path: ':id', component: ViewSystemComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class SystemsRoutingModule { }
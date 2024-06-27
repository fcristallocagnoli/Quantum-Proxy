import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { JobsComponent } from './jobs.component';
import { ViewJobComponent } from './view-job.component';


const routes: Routes = [
    { path: '', component: JobsComponent },
    { path: ':uuid', component: ViewJobComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class JobsRoutingModule { }
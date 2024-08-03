import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgbdModalContent } from '@app/_components/properties.component';
import { System } from '@app/_models';
import { SystemService } from '@app/_services';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { first } from 'rxjs';

@Component({
    templateUrl: 'view-system.component.html',
})
export class ViewSystemComponent implements OnInit {
    bid: string
    system?: System

    constructor(private route: ActivatedRoute, private systemService: SystemService, private modalService: NgbModal) { }

    ngOnInit(): void {
        this.bid = this.route.snapshot.params['bid']
        this.systemService.getByBid(this.bid)
            .pipe(first())
            .subscribe(system => this.system = system);
    }

    openModal() {
        const modalRef = this.modalService.open(NgbdModalContent);
        modalRef.componentInstance.characterization = this.system?.characterization;
    }

    // Convierte tiempo en milisegundos a tiempo de espera con el formato de IonQ
    convertFromMs(millisecStr: string | undefined): string {
        if (millisecStr === undefined) {
            return "N/A";
        }
        let millisec = parseInt(millisecStr);

        // Convertir milisegundos a segundos
        let seconds = Math.floor(millisec / 1000);

        // Calcular días, horas y minutos
        const mins = Math.floor(seconds / 60);
        seconds = seconds % 60;
        const hours = Math.floor(mins / 60);
        const minutes = mins % 60;
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;

        let avgTimeInQueue = "";

        if (days > 30) {
            avgTimeInQueue = "> 1month";
        } else if (days > 1) {
            avgTimeInQueue = `${days}d ${remainingHours}hrs ${minutes}min`;
        } else if (remainingHours > 1) {
            avgTimeInQueue = `${remainingHours}hrs ${minutes}min`;
        } else if (minutes > 1) {
            avgTimeInQueue = `${minutes}min`;
        } else {
            avgTimeInQueue = "< 1min";
        }

        return avgTimeInQueue;
    }

}

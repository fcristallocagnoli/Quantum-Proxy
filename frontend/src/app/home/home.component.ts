import { Component, OnInit } from '@angular/core';
import { HelperService } from '@app/_services/helper.service';

@Component({ templateUrl: 'home.component.html' })
export class HomeComponent implements OnInit {
    highestQubits?: number;
    lowestQueue?: string;

    nProviders? = 0;
    nSystems? = 0;

    lastChecked: Date;

    constructor(private helperService: HelperService) { }

    ngOnInit() {
        // Get the highest number of qubits
        this.helperService.getAggregattion('backends', [
            { $match: { status: { $in: ["online", "running", "available"] } } },
            { $group: { _id: "null", maxQubits: { $max: "$qubits" } } }
        ]).subscribe((response) => {
            this.highestQubits = response[0]['maxQubits'];
        });

        // Get the lowest queue time
        this.helperService.getAggregattion('backends', [
            {
                $match:
                {
                    status: { $in: ["online", "running", "available"] },
                    "queue.type": "avg_time"
                }
            },
            { $group: { _id: "null", minQueue: { $min: { $toInt: "$queue.value" } } } }
        ]).subscribe((response) => {
            this.lowestQueue = this.convertFromMs(response[0]['minQueue']);
        });

        // Count the number of providers
        this.helperService.countDocuments('providers').subscribe((response) => {
            this.nProviders = response['count'];
        });
        // Count the number of systems
        this.helperService.countDocuments('backends').subscribe((response) => {
            this.nSystems = response['count'];
        });

        // Get the last time the systems were checked
        this.helperService.getAggregattion('providers', [
            { $match: { last_checked: { $exists: true } } },
            { $sort: { last_checked: 1 } },
            { $limit: 1 },
            { $project: { _id: 0, last_checked: 1 } }
        ]).subscribe((response) => {
            this.lastChecked = new Date(response[0]['last_checked']);
        });
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
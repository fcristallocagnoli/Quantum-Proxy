export class ThirdParty {
    id?: string;
    name?: string;
}

export class Provider {
    id?: string;
    pid?: string;
    name?: string;
    description?: string | { summary: string, history: string};
    website?: string;
    fromThirdParty?: boolean;
    fetchMethod?: string;
    thirdParty?: ThirdParty;
    systems?: string[];
    lastChecked?: string;
    // To access the attributes of the object using a string key
    [key: string]: any;
}
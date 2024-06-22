export class ThirdParty {
    id?: string;
    name?: string;
}

export class Description {
    short_description?: string;
    long_description?: string;
    history?: string;
}

export class Provider {
    id?: string;
    pid?: string;
    name?: string;
    description?: string | Description;
    website?: string;
    fromThirdParty?: boolean;
    fetchMethod?: string;
    thirdParty?: ThirdParty;
    systems?: string[];
    lastChecked?: string;
    // To access the attributes of the object using a string key
    [key: string]: any;
}
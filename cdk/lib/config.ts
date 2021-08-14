import { Construct, ConstructNode } from "@aws-cdk/core"
/**
 * Creates a config class from cdk.json that is approachable through methods.
 */
export class Config {
    static rootNode: ConstructNode

    static init(root: Construct) { this.rootNode = root.node; }
    static getConfig<T>(key: string): T { return this.rootNode.tryGetContext(key) as T }

    static get api_secret() { return this.getConfig<string>('api_secret') };

}

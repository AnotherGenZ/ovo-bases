import { HttpApi, HttpMethod } from '@aws-cdk/aws-apigatewayv2';
import { LambdaProxyIntegration } from '@aws-cdk/aws-apigatewayv2-integrations';
import { Alias, Runtime, Version } from '@aws-cdk/aws-lambda';
import { PythonFunction } from '@aws-cdk/aws-lambda-python';
import * as cdk from '@aws-cdk/core';
import { RemovalPolicy } from '@aws-cdk/core';
import { Config } from './config';

export class AwsCdkStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const discordApi = new HttpApi(this, 'OvOApi');

    const interactionsHandler = new PythonFunction(this, 'OvOBasesHandler',{
      functionName: 'OvOBases',
      entry: '../ovo-bases-python/main',
      index: 'devispora/ovo_bases/app.py',
      handler: 'lambda_handler',
      runtime: Runtime.PYTHON_3_8,
      environment:{
        api_secret: Config.api_secret
      }, currentVersionOptions: {removalPolicy: RemovalPolicy.RETAIN}      
    });
    const versionLa = new Version(this, 'VersionIH1', {lambda: interactionsHandler, description: 'initial version', removalPolicy:RemovalPolicy.RETAIN});
    const aliasLa = new Alias(this, 'AliasIH1', {version: versionLa, aliasName: 'main'})
    const interactions_integration = new LambdaProxyIntegration({handler: interactionsHandler});

    discordApi.addRoutes({
      path: '/ovobases',
      methods: [HttpMethod.POST],
      integration: interactions_integration
    });

  }
}

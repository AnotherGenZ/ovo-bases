#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { AwsCdkStack } from '../lib/aws-cdk-stack';
import { Config } from '../lib/config';

const app = new cdk.App();
Config.init(app);
new AwsCdkStack(app, 'OvOBasesStack');

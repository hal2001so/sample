from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    core,
)

class HitCounter(core.Construct):

    @property
    def handler(self):
        return self.handler

    def _init_(self, scope: core.Construct, id: str, downstream: _lambda.IFunction, **kwargs):  #Added new parameter for variable 'downstream' with should pass the referenced functions attributes
        super()._init_(scope, id, **kwargs)

        table = ddb.Table(
            self,'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hitcount.handler',
            code=_lambda.Code.asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,  # I know the downstream variable here should be populated from the argument passed via the above init.
                'HITS_TABLE_NAME': table.table_name,
            }
        )
# Cargar desde demo-openrouter: source aws/contexto.sh
# Solo identificadores públicos: este archivo no contiene claves.
export AWS_PROFILE=thepower-aws
export AWS_REGION=eu-north-1
export AWS_DEFAULT_REGION=eu-north-1
export AWS_PAGER=''
export AWS_CLI_AUTO_PROMPT=off
export S16_PROJECT_ID=123456789012
export S16_CLUSTER=s16-thepower
export S16_SERVICE=s16-thepower-api
export S16_REPOSITORY=s16-clasificador
export S16_REGISTRY=123456789012.dkr.ecr.eu-north-1.amazonaws.com
export S16_IMAGE="$S16_REGISTRY/$S16_REPOSITORY:1"
export S16_SECURITY_GROUP=sg-0b634fb83eb28d501
export S16_LOG_GROUP=/s16/thepower/api
export S16_SECRET_ARN=arn:aws:secretsmanager:eu-north-1:123456789012:secret:s16/thepower/openrouter-bDhmgv
export S16_EXECUTION_ROLE=s16-thepower-ecs-execution

# Perfil y región explícitos incluso si había otra sesión en la terminal.
aws_demo() {
    command aws --profile thepower-aws --region eu-north-1 "$@"
}

s16_comprobar_identidad() {
    local s16_actual
    s16_actual="$(aws_demo sts get-caller-identity --query Account --output text)" || return 1
    if [ "$s16_actual" != "$S16_PROJECT_ID" ]; then
        echo 'STOP: la sesión no corresponde al proyecto autorizado.' >&2
        return 1
    fi
    aws_demo sts get-caller-identity
}

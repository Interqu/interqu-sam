import { util } from '@aws-appsync/utils';
import { remove } from '@aws-appsync/utils/dynamodb';

/**
 * Deletes an item with Connection_id `ctx.args.input.Connection_id` and interview_id `ctx.args.input.Interview_id` from the DynamoDB table.
 * @param {import('@aws-appsync/utils').Context<{input: {Connection_id: unknown; Interview_id: unknown;}}>} ctx the context
 * @returns {import('@aws-appsync/utils').DynamoDBDeleteItemRequest} the request
 */
export function request(ctx) {
    const { Connection_id, Interview_id } = ctx.args.input;
    const key = { Connection_id, Interview_id };
    return remove({
        key,
    })
}

/**
 * Returns the deleted item. Throws an error if the operation failed.
 * @param {import('@aws-appsync/utils').Context} ctx the context
 * @returns {*} the deleted item
 */
export function response(ctx) {
    const { error, result } = ctx;
    if (error) {
        return util.appendError(error.message, error.type, result);
    }
    return result;
}

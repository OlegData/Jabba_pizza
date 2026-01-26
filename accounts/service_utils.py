from typing import List

import grpc


def validate_required(
    content: grpc.ServicerContext, request, required_fields: List
) -> None:
    for field in required_fields:
        if not getattr(request, field, None):
            content.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"{field.replace('_', ' ').title()} is required",
            )

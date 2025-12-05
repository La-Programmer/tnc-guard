from typing import Any, Dict, Optional, List
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from responsecode_enum import ResponseCode


class TNCResponse:
    @staticmethod
    def _build_response(
        success: bool, code: int, message: str, data: Any = None
    ) -> Dict[str, Any]:
        return {
            "status": success,
            "responseCode": code,
            "responseMessage": message,
            "responseData": data,
        }

    @staticmethod
    def success_response(
        entity_name: str,
        data: Any = None,
        code: int = ResponseCode.OK,
        action: Optional[str] = None,
        message: Optional[str] = None,
    ):
        entity_name = TNCResponse._format_entity(entity_name, data)
        error_message = None
        if action == "created":
            error_message = f"Failed to create {entity_name}"
        elif action == "updated":
            error_message = f"Failed to update {entity_name}"

        if resp := TNCResponse._check_data(entity_name, data, error_message, action):
            return resp
        action_msg = (
            f"{entity_name} {action} successfully."
            if action
            else f"{entity_name} request successful."
        )
        return TNCResponse._build_response(True, code, message or action_msg, data)

    @staticmethod
    def _format_entity(entity_name: str, data: Any) -> str:
        return f"{entity_name}s" if isinstance(data, list) else entity_name

    @staticmethod
    def _check_data(
        entity_name: str,
        data: Any,
        error_message: Optional[str] = None,
        action: Optional[str] = None,
    ):
        post_actions = ["created", "updated"]
        if not data:
            if action in post_actions:
                return TNCResponse.error_response(error_message)
            return TNCResponse.not_found_response(entity_name, error_message)
        return None

    @staticmethod
    def get_response(entity_name, data, message=None):
        return TNCResponse.success_response(
            entity_name, data, ResponseCode.OK, "gotten", message
        )

    @staticmethod
    def create_response(entity_name, data=None, message=None):
        return TNCResponse.success_response(
            entity_name, data, ResponseCode.CREATED, "created", message
        )

    @staticmethod
    def update_response(entity_name, data=None, message=None):
        return TNCResponse.success_response(
            entity_name, data, ResponseCode.OK, "updated", message
        )

    @staticmethod
    def not_found_response(
        entity_name: str,
        message: Optional[str] = None,
    ):
        return TNCResponse._build_response(
            False, ResponseCode.NOT_FOUND, message or f"{entity_name} not found."
        )

    @staticmethod
    def delete_response(entity_name, is_deleted, message=None, data=None):
        if is_deleted:
            return TNCResponse._build_response(
                True,
                ResponseCode.OK,
                message or f"{entity_name} successfully deleted.",
                data,
            )
        return TNCResponse.error_response(
            f"Failed to delete {entity_name}", ResponseCode.BAD_REQUEST
        )

    @staticmethod
    def conflict_response(
        entity_name: str, message: Optional[str] = None, subject: Optional[str] = None
    ):
        subject_name = subject.capitalize() if subject else "User"
        return TNCResponse._build_response(
            False,
            ResponseCode.CONFLICT,
            message or f"{subject_name} with {entity_name} already exists.",
        )

    @staticmethod
    def login_response(
        entity_name: str, data: Any, success: bool, message: Optional[str] = None
    ):
        if success:
            return TNCResponse._build_response(
                success,
                ResponseCode.OK,
                message or f"{entity_name} logged in successfully.",
                data,
            )
        return TNCResponse.error_response(
            f"{entity_name} login failed.", ResponseCode.BAD_REQUEST
        )

    @staticmethod
    def verify_response(
        entity_name: str, data: Any = None, message: Optional[str] = None
    ):
        if not data:
            return TNCResponse.error_response(
                f"Failed to verify {entity_name}.", ResponseCode.BAD_REQUEST
            )
        return TNCResponse._build_response(
            True,
            ResponseCode.OK,
            message or f"{entity_name} verified successfully",
            data,
        )

    @staticmethod
    def paged_response(
        entity_name: str,
        data: List[Any],
        total: Optional[int] = 0,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        meta_data: Optional[Any] = None,
        message: Optional[str] = None,
    ):
        entity_name = TNCResponse._format_entity(entity_name, data)
        if resp := TNCResponse._check_data(entity_name, data):
            return resp

        response_data = {
            "data": data,
            "total": total,
            "page": page,
            "pageSize": page_size,
            "metaData": meta_data,
        }
        return TNCResponse._build_response(
            True,
            ResponseCode.OK,
            message or f"{entity_name} gotten successfully",
            response_data,
        )

    @staticmethod
    def error_response(
        message: Optional[str] = None, error_code: int = ResponseCode.SERVER_ERROR
    ):
        return TNCResponse._build_response(
            False, error_code, message or "Internal Server Error."
        )

    @staticmethod
    def unauthorized_response(message: Optional[str] = None):
        return TNCResponse._build_response(
            False,
            ResponseCode.UNAUTHORIZED,
            message or "You are Unauthorized, Please provide a valid access token.",
        )

    @staticmethod
    def forbidden_response(message: Optional[str] = None):
        return TNCResponse._build_response(
            False,
            ResponseCode.FORBIDDEN,
            message or "You do not have access to this feature.",
        )

    @staticmethod
    def custom_response(
        message: str,
        response_code: int = ResponseCode.SERVER_ERROR,
        success: bool = False,
        data: Any = None,
    ):
        return TNCResponse._build_response(success, response_code, message, data)

    @staticmethod
    def json(data: BaseModel, status_code: int = ResponseCode.OK):
        """Return explicit JSONResponse (if you want control over headers)."""
        return JSONResponse(content=data, status_code=status_code)

    @staticmethod
    def set_header_data(response: JSONResponse, key: str, data: Any):
        if key and data:
            response.headers[key] = str(data)

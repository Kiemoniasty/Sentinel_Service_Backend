"""Collection of tools for Service Controllers"""

from enums.sentinel_enums import Response, Status


class ServiceTools:
    """Tools for Service Controllers"""

    def service_to_list(self=None, service=None, settings=None):
        """Convert service model to a list object."""
        result = []

        for item in service:
            for subitem in settings:
                if item.setting_guid == subitem.guid:
                    result.append(
                        {
                            "guid": item.guid,
                            "name": item.name,
                            "setting": {
                                "guid": subitem.guid,
                                "status": ServiceTools.value_status(
                                    status=subitem.status
                                ),
                                "address": subitem.address,
                                "frequency": str(subitem.frequency),
                                "response_time": str(subitem.response_time),
                                "number_of_samples": str(subitem.number_of_samples),
                            },
                            "actual_state": ServiceTools.value_actual_state(
                                actual_state=item.actual_state
                            ),
                        }
                    )

        return result

    def query_to_list(self=None, service=None, settings=None):
        """Convert service model to a dictionary object."""
        result = []

        for item in service:
            for subitem in settings:
                if item.setting_guid == subitem.guid:
                    result.append(
                        {
                            "name": item.name,
                            "setting": {
                                "guid": subitem.guid,
                                "status": ServiceTools.value_status(
                                    status=subitem.status
                                ),
                                "address": subitem.address,
                                "frequency": str(subitem.frequency),
                                "response_time": str(subitem.response_time),
                                "number_of_samples": str(subitem.number_of_samples),
                            },
                            "actual_state": ServiceTools.value_actual_state(
                                actual_state=item.actual_state
                            ),
                        }
                    )

        return result

    def valid_status(self=None, status=None):
        """Validate the status."""

        for item in Status:
            if item.value == status.lower():
                return item.name

    def value_status(self=None, status=None):
        """Validate the status."""

        for item in Status:
            if item == status:
                return item.value

    def valid_actual_state(self=None, actual_state=None):
        """Validate the actual state."""

        for item in Response:
            if item.value == str(actual_state).lower():
                return item.name

    def value_actual_state(self=None, actual_state=None):
        """Validate the actual state."""

        for item in Response:
            if item == actual_state:
                return item.value

    def string_to_int(self=None, data=None):
        """Convert string to integer."""
        try:
            return int(data)
        except ValueError:
            return None

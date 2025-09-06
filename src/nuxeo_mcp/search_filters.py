"""Elasticsearch Search Request Filters for security."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class SearchRequestFilter(ABC):
    """Abstract base class for search request filters."""

    @abstractmethod
    def apply(
        self, query: Dict[str, Any], principal: str, groups: List[str]
    ) -> Dict[str, Any]:
        """Apply security filter to the query.

        Args:
            query: The Elasticsearch query to filter
            principal: The user principal making the request
            groups: List of groups the user belongs to

        Returns:
            The filtered query with security constraints applied

        Raises:
            PermissionError: If the user is not allowed to perform the query
        """
        pass

    @abstractmethod
    def get_index_name(self) -> str:
        """Get the target Elasticsearch index name."""
        pass

    @abstractmethod
    def validate_principal(self, principal: str) -> bool:
        """Validate if the principal is allowed to query this index."""
        pass


class DefaultSearchRequestFilter(SearchRequestFilter):
    """Default filter for repository index with ACL filtering."""

    def apply(
        self, query: Dict[str, Any], principal: str, groups: List[str]
    ) -> Dict[str, Any]:
        """Apply ACL security filter to repository queries."""
        if not self.validate_principal(principal):
            raise PermissionError(
                f"Principal {principal} is not allowed to query repository"
            )

        # Build ACL filter with user principal and groups
        principals = [principal] + groups
        acl_filter = {"terms": {"ecm:acl": principals}}

        # Apply filter to query
        if "bool" in query:
            # Query is already a bool query
            bool_query = query["bool"].copy()

            # Add to existing filter clause
            if "filter" in bool_query:
                if isinstance(bool_query["filter"], list):
                    bool_query["filter"] = bool_query["filter"].copy()
                    bool_query["filter"].append(acl_filter)
                else:
                    bool_query["filter"] = [bool_query["filter"], acl_filter]
            else:
                bool_query["filter"] = [acl_filter]

            return {"bool": bool_query}
        else:
            # Wrap query in bool with filter
            return {"bool": {"must": [query], "filter": [acl_filter]}}

    def get_index_name(self) -> str:
        """Get the repository index name."""
        return "nuxeo"

    def validate_principal(self, principal: str) -> bool:
        """Validate principal - any authenticated user can query repository."""
        return bool(principal)


class AuditRequestFilter(SearchRequestFilter):
    """Filter for audit index - admin only access."""

    def apply(
        self, query: Dict[str, Any], principal: str, groups: List[str]
    ) -> Dict[str, Any]:
        """Apply admin-only filter to audit queries."""
        # Check if user is administrator
        if not self._is_admin(principal, groups):
            raise PermissionError(
                f"Principal {principal} is not allowed to query audit index. "
                "Only administrators can access audit logs."
            )

        # Admins can see all audit entries, return query as-is
        return query

    def get_index_name(self) -> str:
        """Get the audit index name."""
        return "audit"

    def validate_principal(self, principal: str) -> bool:
        """Validate principal - only Administrator."""
        return principal == "Administrator"

    def _is_admin(self, principal: str, groups: List[str]) -> bool:
        """Check if user is an administrator."""
        return principal == "Administrator" or "Administrators" in groups


class FilterChain:
    """Chain multiple filters together."""

    def __init__(self, filters: List[SearchRequestFilter]):
        """Initialize filter chain.

        Args:
            filters: List of filters to apply in order
        """
        self.filters = filters

    def apply(
        self, query: Dict[str, Any], principal: str, groups: List[str]
    ) -> Dict[str, Any]:
        """Apply all filters in sequence.

        Args:
            query: The Elasticsearch query to filter
            principal: The user principal making the request
            groups: List of groups the user belongs to

        Returns:
            The filtered query with all security constraints applied
        """
        result = query
        for filter_instance in self.filters:
            result = filter_instance.apply(result, principal, groups)
        return result

    def validate_principal(self, principal: str) -> bool:
        """Validate principal through all filters."""
        return all(f.validate_principal(principal) for f in self.filters)

    def get_index_names(self) -> List[str]:
        """Get all index names from filters."""
        return [f.get_index_name() for f in self.filters]


class WorkflowAuditRequestFilter(SearchRequestFilter):
    """Filter for workflow audit - filters by workflow permissions."""

    def __init__(self):
        """Initialize workflow audit filter."""
        self.base_filter = AuditRequestFilter()

    def apply(
        self, query: Dict[str, Any], principal: str, groups: List[str]
    ) -> Dict[str, Any]:
        """Apply workflow audit filtering.

        This would filter audit events to only show workflow events
        for workflows the user has permission to view.
        """
        # First check admin access
        filtered_query = self.base_filter.apply(query, principal, groups)

        # Add workflow-specific filtering
        # In a real implementation, this would check workflow permissions
        workflow_filter = {"term": {"category": "eventWorkflowCategory"}}

        if "bool" in filtered_query:
            if "filter" in filtered_query["bool"]:
                filtered_query["bool"]["filter"].append(workflow_filter)
            else:
                filtered_query["bool"]["filter"] = [workflow_filter]
        else:
            filtered_query = {
                "bool": {"must": [filtered_query], "filter": [workflow_filter]}
            }

        return filtered_query

    def get_index_name(self) -> str:
        """Get the audit workflow view name."""
        return "audit_wf"

    def validate_principal(self, principal: str) -> bool:
        """Validate principal - delegates to base audit filter."""
        return self.base_filter.validate_principal(principal)

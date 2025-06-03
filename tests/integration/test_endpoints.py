import os
import pytest

# def test_generate_jd_endpoint_health(client):
#     """
#     This test actually calls the OpenAI API via the endpoint and will fail if OpenAI credentials are missing/invalid.
#     """
#     # Simple test job data
#     data = {
#         "title": "Test Engineer",
#         "seniority": "Junior",
#         "skills": ["Python"],
#         "location": "Remote"
#     }
#     response = client.post("/generate-jd", json=data)
    
#     # Basic checks
#     assert response.status_code == 200
#     result = response.get_json()
#     assert "job_description" in result
#     # You may want to assert some expected keywords for sanity
#     assert "Test Engineer" in result["job_description"] or "test engineer" in result["job_description"].lower()
#     assert "Python" in result["job_description"]


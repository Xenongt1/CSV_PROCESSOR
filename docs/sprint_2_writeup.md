# Sprint 2 — Execution Plan

**Goal**: Apply Sprint 1 feedback and deliver the next increment with summary reports, download functionality, and comprehensive monitoring.

**Stories included**:

- Story 3: Generate summary report
- Story 4: Download report (CSV/JSON)
- Story 5: Logging & monitoring

**Expected number of commits**: 6–8 small, meaningful commits

---

## Sprint 1 Retrospective Feedback Applied

### Improvements Identified:

1. ✅ **Add summary report generation and download endpoints**
2. ✅ **Implement comprehensive logging for upload and parsing**

---

## Step-by-Step Tasks & Commits

| Step | Task                                          | Suggested Commit Message                                |
| ---- | --------------------------------------------- | ------------------------------------------------------- |
| 1    | Enhance parser with advanced statistics       | `Add advanced statistical analytics to CSV summary`     |
| 2    | Implement data filtering via query parameters | `Add data filtering support to upload endpoint`         |
| 3    | Create JSON export endpoint                   | `Implement /export/json endpoint for data download`     |
| 4    | Add comprehensive logging system              | `Add structured logging for all API operations`         |
| 5    | Create system info/health endpoint            | `Add /info endpoint for system metadata and health`     |
| 6    | Implement error handling improvements         | `Improve error handling with custom exception handlers` |
| 7    | Add API documentation branding                | `Enhance API documentation with custom branding`        |
| 8    | Write tests for new features                  | `Add unit tests for filtering and export features`      |

---

## Sprint 2 Deliverables

### 1️⃣ Working Features

#### Story 3: Generate Summary Report ✅

**Implementation**: Enhanced `get_csv_summary()` function in `parser.py`

**Features**:

- **Statistical Analysis**: Mean, median, min, max for numeric columns
- **Categorical Analysis**: Unique value counts and top values for text columns
- **Data Quality Metrics**: Missing value counts per column
- **Schema Information**: Column types and delimiter detection

**Example Output**:

```json
{
  "rows": 1000,
  "columns": ["id", "name", "salary", "department"],
  "delimiter": ",",
  "missing_values": { "salary": 0, "phone": 2 },
  "advanced_stats": {
    "salary": {
      "mean": 98884.83,
      "median": 99000.0,
      "min": 30000.0,
      "max": 150000.0
    },
    "department": {
      "unique_count": 5,
      "top_values": { "Engineering": 350, "Sales": 280 }
    }
  }
}
```

#### Story 4: Download Report ✅

**Implementation**: New `/export/json` endpoint

**Features**:

- Accepts CSV file upload
- Returns downloadable JSON file
- Proper content-type headers for file download
- Error handling for invalid files

**Usage**:

```bash
curl -X POST "http://localhost:8000/export/json" \
  -F "file=@data/sample.csv" \
  --output report.json
```

#### Story 5: Logging & Monitoring ✅

**Implementation**: Comprehensive logging system

**Features**:

- **Upload Logging**: Logs filename, size, and processing status
- **Error Tracking**: Detailed error messages with stack traces
- **Performance Monitoring**: Processing time tracking
- **Health Endpoint**: `/info` endpoint for system metadata

**Log Example**:

```
INFO:app.main:Uploading file: large_sample.csv
INFO:app.main:Successfully processed large_sample.csv with 1000 filtered rows
ERROR:app.main:Error processing invalid.csv: Error parsing CSV: ...
```

**Health Endpoint Response**:

```json
{
  "app_name": "CSV Processor Pro",
  "version": "1.0.0",
  "status": "healthy",
  "endpoints": ["/upload", "/export/json", "/info"]
}
```

---

### 2️⃣ Additional Enhancements Delivered

#### Data Filtering System ✅

**Feature**: Query parameter-based filtering on `/upload` endpoint

**Parameters**:

- `filter_col`: Column name to filter by
- `filter_val`: Value to filter for

**Example**:

```bash
curl -X POST "http://localhost:8000/upload?filter_col=department&filter_val=Engineering" \
  -F "file=@data/sample.csv"
```

#### Custom Error Handling ✅

**Implementation**: Professional error responses

**Features**:

- JSON-formatted error messages
- Proper HTTP status codes
- User-friendly error descriptions

#### API Documentation Branding ✅

**Implementation**: Enhanced Swagger UI

**Features**:

- Custom title: "CSV Processor Pro"
- Version information
- Detailed endpoint descriptions
- Interactive testing interface

---

### 3️⃣ Tests Included

**New Test Coverage**:

```python
# Test filtering functionality
def test_parse_csv_with_filter():
    csv_content = b"name,age\nAlice,30\nBob,25"
    data = parse_csv(csv_content, filter_col="name", filter_val="Alice")
    assert len(data) == 1
    assert data[0]["name"] == "Alice"

# Test advanced statistics
def test_get_csv_summary_with_stats():
    csv_content = b"salary\n50000\n60000\n70000"
    summary = get_csv_summary(csv_content)
    assert "advanced_stats" in summary
    assert summary["advanced_stats"]["salary"]["mean"] == 60000.00
```

**Test Execution**:

```bash
PYTHONPATH=. pytest tests/test_parser.py -v
```

---

### 4️⃣ Sprint 2 Review

#### What Was Delivered:

**Story 3: Generate Summary Report** ✅

- Advanced statistical analytics (mean, median, min, max)
- Categorical data analysis (unique counts, top values)
- Data quality metrics (missing values)
- Fully integrated into `/upload` response

**Story 4: Download Report** ✅

- `/export/json` endpoint implemented
- File download with proper headers
- Error handling for invalid uploads

**Story 5: Logging & Monitoring** ✅

- Structured logging for all operations
- Error tracking with detailed messages
- `/info` health endpoint
- Performance monitoring

**Bonus Features** ✅

- Data filtering via query parameters
- Custom error handling
- Enhanced API documentation
- Additional unit tests

#### Screenshots to Include:

1. **Summary Report Output**: Show advanced statistics in API response
2. **JSON Export Download**: Demonstrate file download functionality
3. **Logging Console**: Show structured logs during operations
4. **Health Endpoint**: Display `/info` endpoint response
5. **GitHub Actions**: Show all tests passing with new features

#### Summary Paragraph:

> "In Sprint 2, we successfully implemented summary report generation with advanced statistical analytics, created a JSON export endpoint for data downloads, and established comprehensive logging and monitoring. We applied feedback from Sprint 1 by adding data filtering capabilities and improving error handling. The project now includes 8+ new incremental commits, expanded test coverage, and a health monitoring endpoint. All features are fully tested and integrated with our CI/CD pipeline."

---

### 5️⃣ Final Retrospective

#### What Went Well:

- ✅ **Incremental Development**: Each feature delivered in small, focused commits
- ✅ **Test Coverage**: Comprehensive tests for all new functionality
- ✅ **Error Handling**: Robust error management across all endpoints
- ✅ **Documentation**: Clear API docs with interactive testing
- ✅ **Monitoring**: Production-ready logging and health checks

#### Challenges Overcome:

- **Complex Statistics**: Implemented advanced analytics while maintaining performance
- **File Downloads**: Properly configured headers and content types for downloads
- **Logging Integration**: Balanced detailed logging without performance impact

#### Key Lessons Learned:

1. **Incremental Commits Matter**
   - Small, focused commits make code review easier
   - Clear commit messages document the development journey
   - Easier to debug and rollback if needed

2. **Testing Saves Time**
   - Writing tests alongside features catches bugs early
   - CI/CD automation prevents regressions
   - Comprehensive test coverage builds confidence

3. **Logging is Essential**
   - Structured logging helps debug production issues
   - Performance metrics identify bottlenecks
   - Error tracking improves user experience

4. **Documentation Drives Adoption**
   - Interactive API docs (Swagger) make testing easy
   - Clear examples help users understand features
   - Good documentation reduces support burden

#### Process Improvements for Future Sprints:

1. **Earlier Testing**: Write tests before implementing features (TDD approach)
2. **Code Reviews**: Implement peer review process for quality assurance
3. **Performance Benchmarks**: Add automated performance testing
4. **User Feedback**: Gather feedback from actual users earlier in development
5. **Security Audit**: Implement security scanning in CI/CD pipeline

---

## Sprint 2 Metrics

**Story Points Completed**: 10 (Story 3: 5 points + Story 4: 3 points + Story 5: 2 points)
**Total Story Points (Sprint 1 + 2)**: 18 points ✅ (Complete backlog)
**Commits Made**: 8+ incremental commits
**New Tests Written**: 6+ test cases
**Test Pass Rate**: 100%
**CI/CD Status**: ✅ All workflows passing
**Code Coverage**: Expanded to cover filtering, export, and statistics

---

## Actual Features Delivered (Reference)

Based on the completed work:

### Core Features:

1. ✅ CSV Upload with validation
2. ✅ Intelligent CSV parsing with delimiter detection
3. ✅ Advanced statistical analytics
4. ✅ Data filtering via query parameters
5. ✅ JSON export endpoint
6. ✅ Comprehensive logging system
7. ✅ Health monitoring endpoint
8. ✅ Custom error handling
9. ✅ Enhanced API documentation

### Infrastructure:

1. ✅ GitHub Actions CI/CD
2. ✅ Comprehensive unit tests
3. ✅ MySQL database integration (bonus)
4. ✅ Docker Compose setup (bonus)
5. ✅ Interactive Jupyter notebook (bonus)

---

## Definition of Done Checklist

For Sprint 2, all stories are **DONE** when:

- [x] Code is committed to GitHub (incremental commits)
- [x] Features work as per acceptance criteria
- [x] Unit tests exist and pass locally
- [x] CI/CD pipeline runs successfully
- [x] Logging is implemented for all operations
- [x] Error handling is comprehensive
- [x] Features are demonstrated in Sprint Review
- [x] Retrospective identifies improvements

---

## Final Project Status

**✅ All Sprint 0 Stories Completed**
**✅ All Sprint 1 Stories Completed**
**✅ All Sprint 2 Stories Completed**

**Total Development Time**: 2 Sprints
**Total Commits**: 15+ incremental commits
**Total Tests**: 10+ comprehensive test cases
**CI/CD Status**: Fully automated and passing

---

## Repository Link

[https://github.com/Xenongt1/CSV_PROCESSOR](https://github.com/Xenongt1/CSV_PROCESSOR)

---

## Appendix: Commit History Summary

### Sprint 1 Commits:

1. Setup project folder structure
2. Initialize Git repo and add dependencies
3. Add CSV generator script
4. Add FastAPI app skeleton with /upload endpoint
5. Implement CSV upload endpoint
6. Add CSV parsing function with basic validation
7. Add unit tests for CSV parsing
8. Setup CI/CD workflow to run tests
9. Add requested unit test and support file paths in parser

### Sprint 2 Commits:

1. Add advanced statistical analytics to CSV summary
2. Add data filtering support to upload endpoint
3. Implement /export/json endpoint for data download
4. Add structured logging for all API operations
5. Add /info endpoint for system metadata and health
6. Improve error handling with custom exception handlers
7. Enhance API documentation with custom branding
8. Add unit tests for filtering and export features

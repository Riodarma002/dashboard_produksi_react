# Chart Display Fix - Summary

## Problem
Chart data was not displaying correctly in React dashboard compared to Streamlit version:
- **North JO GAM**: Streamlit showed data up to jam 18, React only showed up to jam 15
- **North JO IC**: Similar issue with hours not matching
- **X-axis**: Not showing all 24 hours (06-O5)

## Root Cause
The frontend was iterating over `chartData.data` array (which only contains hours with data from API) but the x-axis was set to show all 24 hours. This created a mismatch where:
- API returns 13 hours (e.g., hours 07-18)
- X-axis shows 24 hours (06-O5)
- Data array only had 13 values but was being plotted against 24 x-axis positions
- Result: Chart stopped at wrong hour

## Solution Implemented

### 1. Frontend Data Mapping (`frontend/src/App.jsx`)

**Updated `getCumulativeSeries` function:**
```javascript
const getCumulativeSeries = (key, name) => {
  if (!chartData) return [];
  
  // Create a map from API data: hour -> value
  const dataMap = {};
  chartData.data.forEach(d => {
    dataMap[d.hour] = d[key];
  });
  
  // Build cumulative array for all 24 hours
  let sum = 0;
  let lastHourWithData = -1;
  
  // First pass: find the last hour that has data in the API response
  for (let i = ALL_HOURS.length - 1; i >= 0; i--) {
    const hour = ALL_HOURS[i];
    if (dataMap[hour] !== undefined) {
      lastHourWithData = i;
      break;
    }
  }
  
  // Second pass: build cumulative data array
  const data = ALL_HOURS.map((hour, i) => {
    // If we're past the last hour with data, return null (stop chart)
    if (i > lastHourWithData) return null;
    
    // If this hour has data in API response (including explicit 0)
    if (dataMap[hour] !== undefined) {
      sum += dataMap[hour];
      return sum;
    }
    
    // This hour is before last data hour but not in API response
    return null;
  });
  
  return [{ name, data }];
};
```

**Key Changes:**
1. **Create hour-to-value mapping** from API data
2. **Find last hour with data** in the API response
3. **Map to all 24 hours** in ALL_HOURS array
4. **Return null for hours past last data** - this stops the chart line
5. **Accumulate cumulative sum** only for hours with data

### 2. Rainfall Data Mapping

**Updated both OB and CH charts:**
```javascript
{ 
  name: 'Rainfall', 
  type: 'column', 
  data: ALL_HOURS.map(hour => {
    const dataPoint = chartData.data.find(d => d.hour === hour);
    return dataPoint ? dataPoint.rain : 0;
  })
}
```

**Key Changes:**
- Map rainfall data to all 24 hours
- Use 0 for hours without rainfall data
- Ensures rainfall bars align with correct x-axis positions

## How It Works Now

### Example: North JO GAM with data up to jam 18

**API Response:**
```json
{
  "data": [
    {"hour": "07", "ob": 1410, "ch": 0, "rain": 0},
    {"hour": "08", "ob": 1410, "ch": 0, "rain": 0},
    ...
    {"hour": "15", "ob": 440, "ch": 0, "rain": 0},
    {"hour": "16", "ob": 0, "ch": 0, "rain": 0},
    {"hour": "17", "ob": 0, "ch": 0, "rain": 0},
    {"hour": "18", "ob": 0, "ch": 0, "rain": 0}
  ]
}
```

**Frontend Processing:**
1. Creates dataMap: `{"07": 1410, "08": 1410, ..., "15": 440, "16": 0, "17": 0, "18": 0}`
2. Finds lastHourWithData: index 12 (jam 18 in ALL_HOURS array)
3. Maps to ALL_HOURS:
   - Index 0 (06): null (no data)
   - Index 1 (07): 1410 (cumulative)
   - Index 2 (08): 2820 (cumulative)
   - ...
   - Index 9 (15): cumulative value
   - Index 10 (16): flat line (0 added to cumulative)
   - Index 11 (17): flat line (0 added to cumulative)
   - Index 12 (18): flat line (0 added to cumulative)
   - Index 13-23 (19-O5): null (stop chart)

**Result:**
- ✅ X-axis shows all 24 hours (06-O5)
- ✅ Chart line starts at jam 07 (first data)
- ✅ Chart shows flat line for jam 16-18 (explicit 0 values)
- ✅ Chart stops at jam 18 (last hour with data)
- ✅ No line displayed for jam 19-O5 (empty cells in Excel)

## Data Logic Summary

| Excel Cell | API Response | Chart Display |
|------------|--------------|---------------|
| Has number (e.g., 440) | Included with value | Show cumulative line |
| Explicit 0 | Included with 0 | Show flat line (cumulative stays same) |
| Empty cell | Not included | Stop chart (null value) |

## Backend Logic (Already Correct)

The backend API (`api_main.py`) already uses `min_count=1` in pandas groupby:
```python
ob_df = filtered["ob_f"].groupby("Hour LU")["Volume"].sum(min_count=1).reset_index()
```

This correctly distinguishes:
- **Explicit 0 in Excel** → Returns 0 in API
- **Empty cell in Excel** → Returns NaN (not included in API response)

## Testing

Test with all pits to verify:
1. **North JO GAM**: Chart stops at jam 18 ✅
2. **North JO IC**: Chart stops at correct hour (17 for CH, 18 for OB) ✅
3. **X-axis**: Always shows 06-O5 (24 hours) ✅
4. **Line display**: Only shows where data exists ✅
5. **Flat lines**: Shows for hours with explicit 0 (rain/downtime) ✅

## Files Modified

1. `frontend/src/App.jsx`:
   - Updated `getCumulativeSeries` function (lines ~277-318)
   - Updated OB chart rainfall mapping (lines ~470-477)
   - Updated CH chart rainfall mapping (lines ~500-507)

## Status

✅ **COMPLETE** - Chart data now matches Streamlit version exactly
- X-axis shows all 24 hours
- Data line stops at last hour with entry in Excel
- Explicit 0 values show as flat line
- Empty cells stop the chart

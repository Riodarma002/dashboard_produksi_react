// Test script to verify chart data mapping logic
// This simulates the frontend logic to ensure correct mapping

const ALL_HOURS = [
  '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
  'O0', 'O1', 'O2', 'O3', 'O4', 'O5'
];

// Simulate API response for North JO GAM (data up to jam 18)
const mockApiResponse = {
  data: [
    { hour: '07', ob: 1410, ch: 0, rain: 0 },
    { hour: '08', ob: 1410, ch: 0, rain: 0 },
    { hour: '09', ob: 1410, ch: 0, rain: 0 },
    { hour: '10', ob: 1410, ch: 0, rain: 0 },
    { hour: '11', ob: 1410, ch: 0, rain: 0 },
    { hour: '12', ob: 1410, ch: 0, rain: 0 },
    { hour: '13', ob: 1410, ch: 0, rain: 0 },
    { hour: '14', ob: 1410, ch: 0, rain: 0 },
    { hour: '15', ob: 440, ch: 0, rain: 0 },
    { hour: '16', ob: 0, ch: 0, rain: 0 },    // Explicit 0 - rain/downtime
    { hour: '17', ob: 0, ch: 0, rain: 0 },    // Explicit 0 - rain/downtime
    { hour: '18', ob: 0, ch: 0, rain: 0 }     // Explicit 0 - rain/downtime
    // Hours 19-O5 are NOT in API response (empty cells in Excel)
  ]
};

function getCumulativeSeries(chartData, key, name) {
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
  
  console.log(`Last hour with data: ${ALL_HOURS[lastHourWithData]} (index ${lastHourWithData})`);
  
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
}

// Test the function
console.log('\n=== Testing Chart Data Mapping ===\n');
console.log('API Response Hours:', mockApiResponse.data.map(d => d.hour).join(', '));
console.log('X-axis Hours (ALL_HOURS):', ALL_HOURS.join(', '));
console.log('\n--- Processing OB Data ---');

const result = getCumulativeSeries(mockApiResponse, 'ob', 'Cumm Actual OB');
console.log('\nResult:');
console.log(JSON.stringify(result, null, 2));

console.log('\n--- Detailed Mapping ---');
ALL_HOURS.forEach((hour, i) => {
  const value = result[0].data[i];
  const status = value === null ? '❌ No data (stop chart)' : 
                 value === result[0].data[i-1] ? '📊 Flat line (0 added)' :
                 '✅ Data point';
  console.log(`${hour}: ${value !== null ? value : 'null'} ${status}`);
});

console.log('\n=== Expected Behavior ===');
console.log('✅ X-axis shows all 24 hours (06-O5)');
console.log('✅ Chart starts at jam 07 (first data)');
console.log('✅ Chart shows cumulative values up to jam 15');
console.log('✅ Chart shows flat line for jam 16-18 (explicit 0)');
console.log('✅ Chart stops at jam 18 (last hour with data)');
console.log('✅ No line for jam 19-O5 (null values)');
console.log('\n=== Test Complete ===\n');

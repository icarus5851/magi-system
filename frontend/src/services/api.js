export const evaluateMagi = async (context, query) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/evaluate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ context, query })
    });
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("MAGI Error:", error);
    throw error;
  }
};

type Surrendings = {
  pages: number[];
  hasEllipsis: boolean;
};

function range(start: number, end: number): number[] {
  return (new Array(end - start + 1)).fill(undefined).map((_, i) => i + start);
}


// Calculation helpers
export const getSurrendingLeft = (x1: number, x2: number): Surrendings => {
  if (x1 === 1) return { pages: [], hasEllipsis: false };
  if (x2 === 0) { return { pages: [], hasEllipsis: (x1 > 2) }; }
  if (x1 <= x2 + 2) return { pages: range(2, x1 - 1), hasEllipsis: false };
  return { pages: range(x1 - x2, x1 - 1), hasEllipsis: true };
};
export const getSurrendingRight = (x1: number, x2: number, x3: number): Surrendings => {
  console.log(x1, x2, x3);
  
  if (x1 === x3) return { pages: [], hasEllipsis: false };
  if (x2 === 0) { return { pages: [], hasEllipsis: (x1 < x3 - 1) }; }
  if (Math.abs(x1 - x3) <= x2 + 1) return { pages: range(x1 + 1, x3 - 1), hasEllipsis: false };
  return { pages: range(x1 + 1, x1 + x2), hasEllipsis: true };
};

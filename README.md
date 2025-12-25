在數位邏輯與生成藝術的實驗中，我們常探討如何利用極簡的輸入（Low-dimensional input）來驅動複雜的視覺呈現（High-dimensional output）。本計畫設計了一個基於 3-bit 計數器的系統，用以生成 8 幀連續的 32x32 像素圖像，模擬從基礎狀態轉換到高解析度像素矩陣的映射過程。


- **Input**: 3 independent variables (form 8 frames, counter from 000 to 111, $[x_0, x_1, x_2]$)
- **Output**: 1024 dependent variables (32x32 pixel art, each pixel is 0 or 1,[ $y_{0,0} \sim y_{31,31}$])
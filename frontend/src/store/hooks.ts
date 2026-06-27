import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch, RootState } from "./store";

// Typed versions of the standard hooks, so components get full type safety.
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();

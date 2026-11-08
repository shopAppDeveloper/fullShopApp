export type Menu = {
  id: number;
  title: string;
  path?: string;
  newTab: boolean;
  badge?: string;
  submenu?: Menu[];
};

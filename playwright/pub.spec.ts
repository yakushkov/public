// import { test, expect, beforeAll, afterAll } from '@playwright/test';
import { test, expect } from '@playwright/test';
import dotenv from 'dotenv';
import { connect, disconnect } from '../db';
import * as queries from '../queries.sql';


dotenv.config();

let client: any;
let userId: number;
let url: string;
let name1: string;
let name2: string;
let height1: number;
let height2: number;
let lat: string;
let lon: string;
let lat1: string;
let lon1: string;

test.describe('Test', () => {
  test.beforeAll(async () => {
        
    client = await connect();
    userId = Number(process.env.USER_ID!);
    url = process.env.BASE_URL!;
    name1 = process.env.name1!;
    name2 = process.env.name2!;
    height1 = Number(process.env.height1!);
    height2 = Number(process.env.height2!);
    lat = process.env.lat!;
    lon = process.env.lon!;
    lat1 = process.env.lat1!;
    lon1 = process.env.lon1!;
  });
});

  test.afterAll(async () => {
    await queries.updateProfileUser(Number(userId));

    await disconnect();
  });

  test.describe('Создание элемента', () => {
    test('main page is loading', async ({ page }) => {

      await page.goto(url + 'navigation');
      await page.waitForSelector('text="Система"', { timeout: 5000 });
      await expect(page.locator('text="Система"')).toBeVisible();
    });

    test('Элемент подгружен ', async ({ page }) => {

      await page.goto(url + 'sites');
      await page.waitForSelector('text=Наименование', { timeout: 5000 });
      await expect(page.locator('Наименование')).toBeVisible();
    });

    test('Роль: Создание элемента, кнопка создания доступна', async ({ page }) => {
  
      const checkProfile = await queries.queryProfile();
      const profileWithElAdd: string[] = checkProfile.rows.map((item: any) => item.profile_id);
      const randomProfileWithElAdd = Number(profileWithElAdd[Math.floor(Math.random() * profileWithElAdd.length)]);
      await queries.updateProfileUserWithRandomProfile(randomProfileWithElAdd, Number(userId));
      
      await page.goto(url + 'sites');
      await page.waitForSelector('text=Наименование', { timeout: 5000 });
      const addButton = await page.getByLabel('Создать новый').getByRole('button');
      await expect(addButton).toBeVisible();
    });

    test('Отсутствует Роль: Создание элемента, кнопка создания НЕдоступна', async ({ page }) => {

      const resultProfileWithoutElAdd = await queries.queryProfileWithoutElAdd();
      const profileWithoutElAdd: string[] = resultProfileWithoutElAdd.rows.map((item: any) => item.profile_id);
      const randomProfileWithoutElAdd = Number(profileWithoutElAdd[Math.floor(Math.random() * profileWithoutElAdd.length)]);
      await queries.updateProfileUserWithRandomProfile(randomProfileWithoutElAdd, Number(userId));
      
      await page.goto(url + '...');
      await page.waitForSelector('text=Наименование', { timeout: 5000 });
      const addButton = await page.getByLabel('Создать новый').getByRole('button');
      await expect(addButton).toBeHidden();
    });
    test('Создание Элемента1', async ({ page }) => {

      const resultProfileWithElAdd = await queries.queryProfile();
      const profileWithElAdd: string[] = resultProfileWithElAdd.rows.map((item: any) => item.profile_id);
      const randomProfileWithElAdd = Number(profileWithElAdd[Math.floor(Math.random() * profileWithElAdd.length)]);
      await queries.updateProfileUserWithRandomProfile(randomProfileWithElAdd, Number(userId));

      await page.goto(url + '...');
      await page.waitForSelector('text=Наименование', { timeout: 5000 });
      await page.getByLabel('Создать новый').getByRole('button').click();
      await page.waitForSelector('text=...', { timeout: 5000 });
      await page.getByLabel('...').click();

      const input = await page.locator('input[name="Название"]');
      for (let char of name1.split('')) {
        await input.type(char);
      }
      await page.getByLabel('Создать элемент').locator('div').filter({ hasText: /^Тип 1$/ }).getByLabel('Open').click();
      await page.getByRole('option', { name: 'Наименование Типа' }).click();
      await page.getByLabel('Субрегион', { exact: true }).click();
      await page.getByRole('option', { name: 'Москва1' }).click();
      await page.getByLabel('Комментарий').fill('Testing comment');
      await page.getByRole('button', { name: 'Создать' }).click();
      await expect(page.getByLabel(name1).getByText(name1)).toBeVisible();
    });

    
  test.describe('Определение типа элемента и его местоположения', () => {
    test.describe('Тип элемента', () => {
      
      test('3.2.3: Проверка на обязательность полей', async ({ page }) => {
        
        const resultProfileWithElAdd = await queries.queryProfileWithElAdd();
        const profileWithElAdd: string[] = resultProfileWithElAdd.rows.map((item: any) => item.profile_id);
        
        const randomProfileWithElAdd = Number(profileWithElAdd[Math.floor(Math.random() * profileWithElAdd.length)]);
        await queries.updateProfileUserWithRandomProfile(randomProfileWithElAdd, Number(userId));

        let selectEl = await queries.selElement(name1, name...);
        let numberEl = selectEl.rows[0].id;
        if (!numberEl) {
            throw new Error('El is not created');
        }
        let statusEl = await queries.selElID(numberEl);
        if (Number(statusEl) !== num {
          await queries.changeElStatus(num, numberEl);
        }

        await queries.nullElFields(numberEl);
        
        const Url = `${url}.../view/`;
        console.log(Url);
        await page.goto(Url);
        await page.getByLabel('Отправить на согласование руководителю').click()
        await expect(page.getByRole('heading', { name: 'Действие невозможно, заполните поля ниже' })).toBeVisible()
      });
              
      test('Заполнение основных полей El', async ({ page }) => {
        
        const resultProfileWithElAdd = await queries.queryProfileWithElAdd();
        const profileWithElAdd: string[] = resultProfileWithElAdd.rows.map((item: any) => item.profile_id);
        const randomProfileWithSiteAdd = Number(profileWithElAdd[Math.floor(Math.random() * profileWithSiteAddElgth)]);
        await queries.updateProfileUserWithRandomProfile(randomProfileWithSiteAdd, Number(userId));

        let selectBS = await queries.sel_element(nameEl, nameEl...);
        let numberBs = selectBS.rows[0].site_id;
        if (!numberBs) {
            throw new Error('BS is not created');
        }
        const siteUrl = `${url}sites/${numberBs}/view/1`;
        console.log(siteUrl);
        await page.goto(siteUrl);
        await page.getByLabel('Изменить').getByRole('button').click();
        await page.getByRole('spinbutton', { name: 'Высота подвеса антенны, м' }).click();
        await page.getByRole('spinbutton', { name: 'Высота подвеса антенны, м' }).fill(heightRollOut.toString());
        await page.getByLabel('Open').click();
        await page.getByRole('option', { name: '32' }).click();

        await page.getByRole('spinbutton', { name: 'WGS широта, гг' }).click();
        await page.getByRole('spinbutton', { name: 'WGS широта, гг' }).fill(wgsLatRollout);
        await page.getByRole('spinbutton', { name: 'WGS долгота, гг' }).click();
        await page.getByRole('spinbutton', { name: 'WGS долгота, гг' }).fill(wgsLonRollout);
        await page.getByLabel('Сохранить изменения').getByRole('button').click();
      });

      test('3.2.3: Отправка на согласование', async ({ page }) => {
        
        const resultProfileWithSiteAdd = await queries.queryProfileWithSiteAdd();
        const profileWithElAdd: string[] = resultProfileWithSiteAdd.rows.map((item: any) => item.profile_id);
        const randomProfileWithSiteAdd = Number(profileWithElAdd[Math.floor(Math.random() * profileWithElAdd.length)]);
        await queries.updateProfileUserWithRandomProfile(randomProfileWithElAdd, Number(userId));

        let selectEl = await queries.sel_element(nameEl, nameEl...);
        let numberEl = selectEl.rows[0].elId;
        if (!numberEl) {
            throw new Error('El is not created');
        }

        let selectEl = await queries.sel_elementElFields(numberEl)
        
        if (Object.values(selectEl).some(value => value === null)) {
          await queries.setElFields(numberEl, lat, lon, height1, 179);
        }

        let statusEl = await queries.sel_elementElID(numberEl);
        if (Number(statusEl) !== num) {
          await queries.changeElStatus(num, numEl);
        }

        const Url = `${url}.../view/`;
        console.log(Url);
        await page.goto(Url);
        await page.getByLabel('Отправить на согласование руководителю').click()
        await expect(page.getByLabel('На согласовании у рук.').getByText('На согласовании у рук.')).toBeVisible()
      });
    });
  });
});
const { defaultsDeep, last } = require('lodash');
const request = require('request-promise');
const { retry } = require('@lifeomic/attempt');
const { jar } = require('request');
const { MemoryCookieStore } = require('tough-cookie');
const cheerio = require('cheerio');
const debug = require('debug')('bot:dizu:api');

const defaultOptions = (cookieJar, headers) => {
  return {
    baseUrl: 'https://dizu.com.br',
    jar: cookieJar,
    gzip: true,
    headers: headers,
    method: 'GET',
    resolveWithFullResponse: true,
  }
};

const headers = {
  'Accept': `*/*`,
  'Host': `dizu.com.br`,
  'User-Agent': `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36`,
  'Accept-Language': `pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7`,
  'Accept-Encoding': `gzip`,
  'Connection': `keep-alive`,
  'X-Requested-With': `XMLHttpRequest`,
  'cache-control': `no-cache`,
  'pragma': `no-cache`,
  'sec-ch-ua': `"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"`,
  'sec-ch-ua-mobile': `?0`,
  'sec-fetch-dest': `empty`,
  'sec-fetch-mode': `cors`,
  'sec-fetch-site': `same-origin`,
};

class DizuAPI {
  constructor() {
    this.cookieStore = new MemoryCookieStore();
    this.cookieJar = jar(this.cookieStore);

	  const cookies = `__cfduid=d67c87f22941c4798da92da82a41ba6b71616677462;
	  __cf_bm=bcef4b9acb7691c1aec0e02d36fb3b3144a7f05b-1616677464-1800-Aa0/X3xnOQum2EfA/K0VtCxTnQg5+dhQbx6bGFIcHOfQmvjeFgHJvfvuW9UKyzGmvF2stp03uPM6/9ozWSNCBNPLyvM7AxurLvK2CR1wh/BJg/ToXGdYPjksCooSwcjuiQ==;
	  _ga=GA1.3.974360772.1616677466;
	  _gid=GA1.3.308710921.1616677466;
	  crsftoken=144c365f857d6269ff46d1bb11839927:a4035c207b3a75191370ff3db541487b;
	  _gat_gtag_UA_160075623_1=1`;
    for (let cookie of cookies.split(`;`)) {
      this.cookieJar.setCookie(cookie, `https://dizu.com.br/`);
    }

    this.attemptOptions = {
      maxAttempts: 100,
      delay: 3000,
      factor: 1.2,
      handleError: (error, context, options) => {
        console.error(error);
        console.error(context);
        console.error(options);
      }
    };
  }

  async send(options) {
    return retry(async () => request(defaultsDeep({}, options, defaultOptions(this.cookieJar, headers))), this.attemptOptions);
  }

  async getTask(accountId) {
    let data = null;
    let response = null;

    await retry(async () => {
      try {
        const url = this.getTaskUrl(accountId);
        response = await this.send({ url });

        const $ = cheerio.load(response.body);

        const username        = last($('a#conectar_step_4').attr('href').split('/'));
        const connectFormId   = $('#conectar_form_id').attr('value');
        const accountIdAction = $('#conta_id_acao').attr('value');

        data = {
          username,
          connectFormId,
          accountIdAction,
        };

        debug(data);
      } catch (e) {
        console.log(response);

        throw e;
      }
    }, this.attemptOptions);

    return data;
  }

  async submitTask(taskId, accountId) {
    const form = {
      tarefa_token: null,
      tarefa_id: taskId,
      conta_id: accountId,
      realizado: 1,
    };

    const response = await this.send({ url: '/painel/confirmar_pedido', method: 'POST', form });
    debug(response.body);
    return response.body;
  }

  getTaskUrl(accountId) {
    return `/painel/listar_pedido/?&conta_id=${accountId}&twitter_id=Twitter&tiktok_id=TikTok&tarefa10=0&curtida05=0&acoesmg=0`;
  }
}

module.exports = DizuAPI;

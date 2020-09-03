    def add_to_DB(self, _res):
        try:
            # buffer = []
            # for _record in _res:
            #     buffer.append(_record)
            #     if len(buffer) % 10000 == 0:
            #         self.session.bulk_insert_mappings(buffer)
            #         buffer = []

            ins = self.table.insert().values(
                project_name=_res[0],
                state_name=_res[1],
                area_name=_res[2],
                tenure=_res[3],
                building_type=_res[4],
                RM_median_price=_res[5],
                RM_num_transactions=_res[6]).prefix_with('IGNORE')
            print(str(ins))  # --> to see the SQL command

            ins.compile().params
            result = self.DB_connection.execute(ins)

            self.trans.commit()
            return True

        except Exception as e:
            _logger.error('Exception %s', e)
            print_exception(e, exitStatus=False)
            return None

    def grab_onepage_edgeprop(self, page):
        try:
            time.sleep(5)
            self.driver.get(self.config["property_url_second"]+page)
            time.sleep(2)
            _trs = self.driver.find_elements_by_xpath("//tbody/tr")
            for _tr in _trs:
                _tds = _tr.find_elements_by_tag_name('td')

                # state , area
                _ps = _tds[0].find_elements_by_tag_name('p')
                _project_name = _ps[0].text
                _content = _ps[1].text
                # _content = _content.replace('"','').replace(",","")
                parts = _content.split(',')
                _area = parts[0].strip()
                _state = parts[1].strip()

                # tenure, building type
                _ps = _tds[1].find_elements_by_tag_name('p')
                _tenure = _ps[0].text
                _building_type = _ps[1].text

                # 	Median Price Psf
                _median_price_psf = float(_tds[2].text.split(' ')[1].replace(',',''))

                # 	Median Price
                _median_price = float(_tds[3].text.split(' ')[1].replace(',',''))

                # 	number Transactions
                _num_transaction = int(_tds[4].find_element_by_tag_name('a').text.split(' ')[0])

                _result = [_area,_state,_tenure, _building_type,  _median_price_psf,  _median_price, _num_transaction]
                self.add_to_DB(_result)
            return True
        except Exception as e:
            _logger.error('Exception %s', e)
            print_exception(e, exitStatus=False)
            return None

    # from selenium.webdriver.support.ui import Select
    def property_stats(self):
        try:
            self.driver.get(self.config['property_url_first'])
            # self.driver.implicitly_wait(50)
            delay = 10  # seconds
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'state')))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")

            # # drop-down menu clicking, works fine
            # _options = self.driver.find_elements_by_tag_name('select')[0].find_elements_by_tag_name("option")
            # for option in _options:
            #     if option.text == 'KUALA LUMPUR':
            #         option.click()  # select() in earlier versions of webdriver
            #         break
            #
            # time.sleep(5)
            # _options2 = self.driver.find_elements_by_tag_name('select')[1].find_elements_by_tag_name("option")
            # for option in _options2:
            #     if option.text == 'Bangsar':
            #         option.click()  # select() in earlier versions of webdriver
            #         break

            _pages = self.driver.find_elements_by_xpath("//ul[@class='pagination']/li")
            _ps = _pages[len(_pages)-1].text

            _bulk_result = []
            for _i in range(1,int(_ps)+1):

                # time.sleep(5)
                _ret_val = self.grab_onepage_edgeprop( str(_i))


            return True
        except Exception as e:
            _logger.error('Exception %s', e)
            print_exception(e, exitStatus=False)
            return None


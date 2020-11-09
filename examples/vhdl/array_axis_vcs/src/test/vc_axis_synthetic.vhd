-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this file,
-- You can obtain one at http://mozilla.org/MPL/2.0/.
--
-- Copyright (c) 2014-2020, Lars Asplund lars.anders.asplund@gmail.com

architecture synthetic of vc_axis is

  signal valid, ready, last : std_logic;
  signal data : std_logic_vector(data_length(m_axis)-1 downto 0);

begin

    vunit_axism: entity vunit_lib.axi_stream_master
    generic map (
      master => m_axis
    )
    port map (
      aclk   => clk,
      tvalid => valid,
      tready => ready,
      tdata  => data,
      tlast  => last
    );

    vunit_axiss: entity vunit_lib.axi_stream_slave
    generic map (
      slave => s_axis
    )
    port map (
      aclk   => clk,
      tvalid => valid,
      tready => ready,
      tdata  => data,
      tlast  => last
    );

end architecture;
